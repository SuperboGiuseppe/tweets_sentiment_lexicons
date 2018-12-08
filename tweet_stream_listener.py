#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = "Emre Arkan"
__copyright__ = "Copyright 2018, Project for Natural Language Processing and Text Mining, University of Oulu"
__email__ = "emrearkan@outlook.de"

import json
import os

from tweepy import StreamListener


class TweetStreamListener(StreamListener):

    def __init__(self, filepath):
        super(TweetStreamListener, self).__init__()
        self.num_of_tweets = 0
        self.filepath = filepath

    def on_status(self, status):
        """
        This method overloads the on_status from StreamListener
        every time there is a new status it gets the json format from it and stores it in 'tweets.json'
        in the same path as the program
        :param status:
        :return:
        """
        try:
            with open(self.filepath, 'a', encoding='utf8') as f:
                json_string = json.dumps(status._json, ensure_ascii=False)  # escaping unicode charachters
                if self.num_of_tweets != 0:
                    json_string = str(',\n\t' + json_string)
                else:
                    json_string = str('\t' + json_string)
                f.write(json_string)
                f.flush()
                os.fsync(f.fileno())
                self.num_of_tweets += 1
                if self.num_of_tweets % 10 == 0:
                    print("Running...", self.num_of_tweets, "tweets have been saved!")
        # Error handling
        except BaseException as e:
            print("Error on_status: %s", str(e))

    def on_error(self, status):
        print(status)
        return True

    def on_timeout(self):
        return True
