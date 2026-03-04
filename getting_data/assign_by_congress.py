import json

folders = ["", "min_"] # this only works in this specific way. this is not truely abstracted.
folder = 'by_congress'

for _ in folders:
    folder = _ + folder # this would be what would break if i had a 3rd path, but i dont. so.
    with open("./public/data/min_members.json", "r") as f:
        data = json.load(f)

    congress = {}

    for member in data:
        to_date_terms = [] # have to make sure the terms of the person does not exceed their
        for term in member['terms']:
            to_date_terms.append(term)
            try:
                congress[term["congress"]].append({"yob": member["yob"], "terms": to_date_terms})
            except:
                congress[term["congress"]] = [{"yob": member["yob"], "terms": to_date_terms}]

    for key in congress:
        with open(f"./public/data/{folder}/{key}.json", "w") as f:
            f.write(json.dumps(congress[key]))