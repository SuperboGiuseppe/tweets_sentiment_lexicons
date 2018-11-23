#!/usr/bin/python
# -*- encoding: utf-8 -*-

import json
import os

from tweepy import StreamListener


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
