#!/bin/env python3

import praw
import datetime
import os
from twilio.rest import Client
from configparser import ConfigParser

# Define ConfigParser values
file = 'secretstuff/config.ini'
config = ConfigParser()
config.read(file)

# Define Reddit values
reddit = praw.Reddit(
    client_id = config['reddit']['clientID'],
    client_secret = config['reddit']['clientSecret'],
    user_agent = config['reddit']['userAgent'],
)
subreddit = reddit.subreddit("buildapcsales")

# Define Twilio values
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# Define filters
graphicsCard = "3080"
processorUnit = "12700K"
monitor = "1440p"

def monitorComments(client, gpu, cpu, monitor, sub):
    while True:
        for submission in sub.stream.submissions(skip_existing=True):
            if gpu in submission.title or cpu in submission.title or monitor in submission.title:
                timestamp = submission.created_utc
                postTime = datetime.datetime.fromtimestamp(timestamp)
                postTitle = submission.title
                postLink = ("https://www.reddit.com" + submission.permalink)
                postUrl = (submission.url)
                sendMessage(client, postTime, postTitle, postLink, postUrl)

def sendMessage(client, postTime, postTitle, postLink, postUrl):
    messageBody = [postTime, postTitle, postLink, postUrl]

    message = client.messages.create(
            body = (""" 
{}
{} 

{}

{}
""").format(messageBody[0], messageBody[1], messageBody[2], messageBody[3]),
            from_= ['twilio']['phoneNumber'],
            to=['client']['phoneNumber']
        ) 

try:
    monitorComments(client, graphicsCard, processorUnit, monitor, subreddit)     

except KeyboardInterrupt:
    print("Ended")