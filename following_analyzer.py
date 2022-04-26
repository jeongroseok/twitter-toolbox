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

    followings = []
    try:
        for user_id in friend_ids:
            user = api.get_user(user_id=user_id)

            print(f" * {user.name} {user.screen_name}")
            print(f"   followers_count: {user.followers_count}")
            print()

            followings.append(
                {
                    "id": user.id,
                    "name": user.name,
                    "screen_name": user.screen_name,
                    "profile_image_url": user.profile_image_url,
                    "followers_count": user.followers_count,
                    "followings_count": user.friends_count,
                }
            )
    except KeyboardInterrupt:
        print(f" * count: {len(followings)}")
    finally:
        with open(f"followings_{int(time())}.json", "w") as fp:
            json.dump(followings, fp)


if __name__ == "__main__":
    main()
