#!/usr/bin/python
# -*- encoding: utf-8 -*-

from tweepy import OAuthHandler
from tweepy import Stream

from tweet_stream_listener import TweetStreamListener


def main():
    authentication = {}
    with open("keys.txt", 'r') as f:
        data = f.read().split("\n")
        authentication['consumer_key'] = data[0]
        authentication['consumer_secret'] = data[1]
        authentication['access_token'] = data[2]
        authentication['access_token_secret'] = data[3]

    # bounding box including norway, sweden, denmark, finland
    locations = [4.2092555141, 53.6745095307, 31.9825448447, 71.2355120003]

    auth = OAuthHandler(authentication.get('consumer_key'), authentication.get('consumer_secret'))
    auth.set_access_token(authentication.get('access_token'), authentication.get('access_token_secret'))
    # auth_api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # wait_on_rate_limit ensures that the connection is kept alive
    # even if Twitter standard Stream API blocks requests until the wait time is done.
    twitter_stream = Stream(auth, TweetStreamListener(), tweet_mode="extended", wait_on_rate_limit=True)

    try:
        with open('tweets/tweets.json', 'w+', encoding='utf8') as f:
            f.write('[\n')
        twitter_stream.filter(locations)
    except KeyboardInterrupt:
        with open('tweets/tweets.json', 'a', encoding='utf8') as f:
            f.write("\n]")
        exit(0)


if __name__ == '__main__':
    main()
