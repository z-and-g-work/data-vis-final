import json

folders = ["", "min_"]
folder = 'by_congress'

for _ in folders:
    folder = _ + folder
    with open("./public/data/min_members.json", "r") as f:
        data = json.load(f)

    congress = {}

    for member in data:
        to_date_terms = [] # have to account for early years
        for term in member['terms']:
            to_date_terms.append(term)
            try:
                congress[term["congress"]].append({"yob": member["yob"], "terms": to_date_terms})
            except:
                congress[term["congress"]] = [{"yob": member["yob"], "terms": to_date_terms}]

    for key in congress:
        with open(f"./public/data/{folder}/{key}.json", "w") as f:
            f.write(json.dumps(congress[key]))