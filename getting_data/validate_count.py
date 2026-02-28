# all of these should have a len of each congress. each should have 535: 100 senate and 435 reps. at least after alask and hawaii 
# became the 49 and 50th states in 1959 increasing senate to 100 members (two per state). reps changed to 435 in 1910.

import json

# narrowed it down to 86 - 119 (1959 - 2027)
for i in range(86, 120):
    with open(f"./public/data/by_congress/{i}.json") as f:
        data = json.load(f)

    print(f"congress {i}\t{len(data)} members")