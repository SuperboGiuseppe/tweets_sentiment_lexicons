import json
import os

import tweepy
from tweepy import OAuthHandler, StreamListener


class TweetStreamListener(StreamListener):

    def __init__(self):
        super(TweetStreamListener, self).__init__()
        self.x = 0

    def on_status(self, status):
        """
        This method overloads the on_status from StreamListener
        every time there is a new status it gets the json format from it and stores it in 'tweets.json'
        in the same path as the program
        :param status:
        :return:
        """
        try:
            with open('tweets/tweets.json', 'a', encoding='utf8') as f:
                json_string = json.dumps(status._json, ensure_ascii=False)  # escaping unicode charachters
                if self.x != 0:
                    json_string = str(',\n\t' + json_string)
                else:
                    json_string = str('\t' + json_string)
                f.write(json_string)
                f.flush()
                os.fsync(f.fileno())
                self.x += 1
                if self.x % 10 == 0:
                    print("Running... ", self.x, " tweets have been saved!")
        # Error handling
        except BaseException as e:
            print("Error on_status: %s", str(e))

    def on_error(self, status):
        print(status)
        return True

    def on_timeout(self):
        return True


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
    twitter_stream = tweepy.Stream(auth, TweetStreamListener(), tweet_mode="extended", wait_on_rate_limit=True)

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
