#!/usr/bin/python3

#############################################################################################
#                               Program by Mohammed Faisal Khan                             #
#                               00598949                                                    #
#                               mkhan8@unh.newhaven.edu                                     #
#                               Created on February 6, 2018                                 #
#############################################################################################

# Importing modules
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os
from pymongo import MongoClient
import json

# API Initialization

ckey = 'TUmVragHR1yEEOlHIfxM9GESS'  # '**CONSUMER KEY**'
consumer_secret = 'bALCr10bNrredcAnKSJqNfoyHBkrqt4g8WevNJkXq2ao11FyqG'  # '**CONSUMER SECRET KEY***'
access_token_key = '106049147-lvkgyFcULiYIBYv0azMPxx4EptB4S3LSiCHKoLmb'  # '**ACCESS TOKEN**'
access_token_secret = 'RfTo8ITCRwjzOcZHue9QmpgI1LcMh4nOwxVcZYj693Qpm'  # '**ACCESS TOKEN SECRET**'

start_time = time.time()  # grabs the system time
keyword_list = ['disaster, earthquake, tsunami, storm, flood, fire']  # track list

# Function Definitions

# Classes

# Listener Class Override


class Listener(StreamListener):

    def __init__(self, start_time, time_limit=60):
        self.time = start_time
        self.limit = time_limit

    def on_data(self, data):

        while (time.time() - self.time) < self.limit:

            try:
                client = MongoClient('localhost', 27017)
                db = client['twitter_db']
                collection = db['twitter_collection']
                tweet = json.loads(data)
                collection.insert(tweet)
                return True

            except BaseException as e:
                print('failed ondata,', str(e))
                time.sleep(5)
                pass

        exit()

    def on_error(self, status):
        print(status)

#############################################################################################

# Main Program


auth = OAuthHandler(ckey, consumer_secret)  # OAuth object
auth.set_access_token(access_token_key, access_token_secret)


twitterStream = Stream(auth, Listener(start_time, time_limit=20))  # initialize Stream object with a time out limit
twitterStream.filter(track=keyword_list, languages=['en'])  # call the filter method to run the Stream Object

#############################################################################################
#                                       End of Program                                      #
#                                     Copyright (c) 2017                                    #
#############################################################################################
