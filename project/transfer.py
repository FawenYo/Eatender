import config

config.db.vote.delete_many({})

all_data = config.db.vote_pull.find({})
total_count = all_data.count()
index = 0

for each in all_data:
    index += 1
    restaurants = []
    for i in each["restaurants"]:
        restaurants.append(i["place_id"])
    participants = {}
    for a_i, a_v in each["participants"].items():
        participants[a_i] = {"restaurants": a_v, "time": []}
    data = {
        "_id": each["_id"],
        "restaurants": restaurants,
        "creator": each["creator"],
        "vote_name": "吃飯投票",
        "vote_end": "2021/1/1",
        "start_date": "2021/1/1",
        "num_days": 1,
        "min_time": 7,
        "max_time": 22,
        "create_time": each["create_time"],
        "participants": participants,
    }
    config.db.vote.insert_one(data)
    print(f"{total_count - index} left")
