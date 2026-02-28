import requests
from dotenv import load_dotenv
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

api_key = os.getenv("CONGRESS_API_KEY")
base_url = "https://api.congress.gov/v3"

# I nicely asked claude to use subprocesses cause I did the math and it would have been at least a few days - i do think i over estitmated the time, but with this it was 60x faster and took a few min, so it would have taken a few HOURS 

# ── 1. Fetch all members ──────────────────────────────────────────────────────
members = []
offset = 0
limit = 250

url = f"{base_url}/member"

while True:
    params = {
        "api_key": api_key,
        # "currentMember": "true",
        "limit": limit,
        "offset": offset,
        "format": "json"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    batch = data.get("members", [])
    if not batch:
        break

    members.extend(batch)

    total = data.get("pagination", {}).get("count", 0)
    offset += limit
    if offset >= total:
        break

print(f"Fetched {len(members)} members. Starting parallel detail fetch...")

# ── 2. Fetch each member's detail in parallel ─────────────────────────────────
def fetch_member(member):
    """Returns (index, useful_data, extra_useful_data, log_entry_or_None)"""
    bio_id = member["bioguideId"]
    url = f"{base_url}/member/{bio_id}"
    params = {"api_key": api_key, "format": "json"}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        m = response.json()["member"]

        data = {
            "yob": m.get("birthYear", 0),
            "terms": m.get("terms", 0)
        }
        extra_data = {
            "yob": m.get("birthYear", 0),
            "terms": m.get("terms", []),
            "state": m.get("state", ""),
            "img": m.get("depiction", {}).get("imageUrl", ""),
            "name": m.get("directOrderName", ""),
            "district": m.get("district", 0)
        }
        return (member, data, extra_data, None)

    except Exception as e:
        empty = {"yob": 0, "terms": 0}
        empty_extra = {"yob": 0, "terms": [], "state": "", "img": "", "name": "", "district": 0}
        return (member, empty, empty_extra, f"{bio_id} epicly failed! {e}")


MAX_WORKERS = 60 # claude rec - well see if we hit the 5000 / hour rate limit - at that rate it might take 4 hours? congress has had 10,000 

useful_data = [None] * len(members)
extra_useful_data = [None] * len(members)
logs = []
completed = 0

# Use a dict to preserve original order
index_map = {m["bioguideId"]: i for i, m in enumerate(members)}

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {executor.submit(fetch_member, m): m for m in members}

    for future in as_completed(futures):
        member, data, extra_data, log = future.result()
        idx = index_map[member["bioguideId"]]
        useful_data[idx] = data
        extra_useful_data[idx] = extra_data
        if log:
            logs.append(log)

        completed += 1
        if completed % 10 == 0 or completed == len(members):
            print(f"  {completed}/{len(members)} ({round(100 * completed / len(members), 1)}%)")

# ── 3. Write output ───────────────────────────────────────────────────────────
os.makedirs('./public/data', exist_ok=True)

with open('./public/data/min_members.json', 'w') as f:
    json.dump(useful_data, f)

with open('./public/data/members.json', 'w') as f:
    json.dump(extra_useful_data, f)

with open('./public/data/logs.txt', 'w') as f:
    f.write('\n'.join(logs))

print(f"Done! {len(logs)} errors logged.")