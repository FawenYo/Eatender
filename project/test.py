import config

data = []

for each in config.db.vote_pull.find():
    temp = {}
    temp["_id"] = each["_id"]
    temp["restaurants"] = each["restaurants"]
    temp["creator"] = each["creator"]
    temp["vote_name"] = each["vote_name"]
    temp["due_date"] = each["due_date"]
    temp["dates"] = each["dates"]
    temp["create_time"] = each["create_time"]
    temp["result"] = {}
    temp["result"]["restaurants"] = each["result"]["restaurants"]
    temp["result"]["dates"] = each["result"]["dates"]
    temp["result"]["best"] = {}
    temp["result"]["user"] = {}
    for x in each["result"]["dates"]:
        test_1, test_2, test_3 = x.split(" ")
        for y in each["result"]["restaurants"]:
            temp["result"]["best"][f"{test_1} {test_2} + {test_3} @ {y}"] = []
    for user, info in each["result"]["user"].items():
        temp["result"]["user"][user] = {}
        temp["result"]["user"][user]["dates"] = each["result"]["user"][user]["dates"]
        a = []
        for i in each["result"]["user"][user]["restaurants"]:
            rid = each["restaurants"][i]
            a.append(i)
        temp["result"]["user"][user]["restaurants"] = a
        for z in each["result"]["user"][user]["dates"]:
            z_1, z_2, z_3 = z.split(" ")
            for f in each["result"]["user"][user]["restaurants"]:
                rid = each["restaurants"][f]
                temp["result"]["best"][f"{z_1} {z_2} + {z_3} @ {rid}"].append(user)
    data.append(temp)

config.db.vote.insert_many(data)
