import json

with open("removed_followers_1648486006.json") as fp:
    users = json.load(fp)

    max_followers_count = 0
    screen_name = ""
    for user in users:
        if user["followers_count"] > max_followers_count:
            max_followers_count = user["followers_count"]
            screen_name = user["screen_name"]
    print(screen_name)
