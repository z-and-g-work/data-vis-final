# just felt like it was not needed to get this information every time someone goes on the page - kinda a lame thing to do with a free api
import requests
from dotenv import load_dotenv
import json
import os
import tqdm

load_dotenv()

api_key = os.getenv("CONGRESS_API_KEY")
base_url = "https://api.congress.gov/v3"

# max per request is 250. loop that baby its inf
members = []
offset = 0
limit = 250 # max for our data source

url = f"{base_url}/member"
params = {
    "api_key": api_key,
    "currentMember": "true",
    "limit": limit,
    "offset": offset,
    "format": "json"
}

while 1:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    batch = data.get("members", [])
    if not batch:
        break

    members.extend(batch)

    # Check if there are more pages
    total = data.get("pagination", {}).get("count", 0)
    offset += limit

    if offset >= total:
        break
    else: break

useful_data = []
extra_useful_data = [] # kinda a misnomer
logs = []
# get yob and terms
for i, member in enumerate(members):
    if not i % 5:
        print(f"Out of {len(members)} you've done \t{round(100 * i / len(members), 2)}%\t aka {i}")

    url = f"{base_url}/member/{member['bioguideId']}"
    params = {
        "api_key": api_key,
        "format": "json"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    too_much_data = response.json()

    data = {'yob': 0, 'terms': 0}
    extra_data = {'yob': 0, 'terms': [], 'state': '', 'img': '', 'name': '', 'district': 0}

    try:
        data["yob"] = too_much_data['member']['birthYear']
        data["terms"] = too_much_data['member']['terms']
        extra_data["yob"] = too_much_data['member']['birthYear']
        extra_data["terms"] = too_much_data['member']['terms']
        extra_data["state"] = too_much_data['member']['state']
        extra_data["name"] = too_much_data['member']['directOrderName']
        extra_data["img"] = too_much_data['member']['depiction']['imageUrl']
        extra_data["district"] = too_much_data['member']['district']
    except Exception as e:
        logs.append(f"{member['bioguideId']} epicly failed! {e}")

    useful_data.append(data)
    extra_useful_data.append(extra_data)

with open('./public/data/min_members.json', 'w') as f:
    f.write(json.dumps(useful_data))

with open('./public/data/members.json', 'w') as f:
    f.write(json.dumps(extra_useful_data))

with open('./public/data/logs.txt', 'w') as f:
    f.write('\n'.join(logs))