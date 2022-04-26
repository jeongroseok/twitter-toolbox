import json
import random
from time import time

import tweepy

import config
from utils import process_access_token


def main():
    auth_handler = tweepy.OAuth1UserHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)

    process_access_token(auth_handler)

    api = tweepy.API(auth_handler)

    print(f"Logged In via {api.verify_credentials().screen_name}")

    friend_ids = api.get_friend_ids()
    random.shuffle(friend_ids)

    removed_friend_ids = []
    try:
        for user_id in friend_ids:
            user = api.get_user(user_id=user_id)

            # 맞팔이면서
            if user.following:
                # 게시물이 존재하고
                timeline = api.user_timeline(user_id=user_id)
                # 게시물이 2021년 이후에도 존재할때만
                if user.following and len(timeline) > 0:
                    if user.following and timeline[0].created_at.year > 2020:
                        print(f" * {user.name} {user.screen_name}")
                        continue

            print(f" * {user.name} {user.screen_name}")
            print(f"   followers_count: {user.followers_count}")
            print()

            api.create_block(screen_name=user.screen_name)
            api.destroy_block(screen_name=user.screen_name)

            removed_friend_ids.append(user._json)

    except KeyboardInterrupt:
        with open(f"removed_friend_ids_{int(time())}.json", "w") as fp:
            json.dump(removed_friend_ids, fp)


if __name__ == "__main__":
    main()
