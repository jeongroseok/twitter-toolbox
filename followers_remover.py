import json
from time import time

import tweepy

import config
from utils import process_access_token


def main():
    auth_handler = tweepy.OAuth1UserHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)

    process_access_token(auth_handler)

    api = tweepy.API(auth_handler)

    print(f"Logged In via {api.verify_credentials().screen_name}")

    followers = api.get_follower_ids()
    removed_followers = []
    try:
        for user_id in followers:
            user = api.get_user(user_id=user_id)

            # if check_hangul(user.name):
            #     continue
            # if check_hangul(user.description):
            #     continue
            # 팔로워가 5000보다 적은 계정
            # if user.followers_count > 5000:
                # continue
            # 팔로워가 10명이 넘지 않는 잠금 계정
            # if user.protected and user.followers_count > 10:
            #     continue
            # 맞팔이 아닌 계정
            if user.following:
                continue

            print(f" * {user.name} {user.screen_name}")
            print(f"   followers_count: {user.followers_count}")
            print()

            api.create_block(screen_name=user.screen_name)
            api.destroy_block(screen_name=user.screen_name)

            removed_followers.append(user._json)

    except KeyboardInterrupt:
        with open(f"removed_followers_{int(time())}.json", "w") as fp:
            json.dump(removed_followers, fp)


if __name__ == "__main__":
    main()
