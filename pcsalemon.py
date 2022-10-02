#!/bin/env python3
import praw
import datetime
import os
from twilio.rest import Client
from configparser import ConfigParser

# Define ConfigParser values
file = 'config.ini'
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
    partList = [gpu, cpu, monitor]
    # Infinite loop to keep bot running, might be redundant
    while True:
        # This for loop may already run infinitely
        for submission in sub.stream.submissions(skip_existing=True):
            title = submission.title
            for part in partList:
                if part in title:
                    # Gather post content for message
                    timestamp = submission.created_utc
                    postTime = datetime.datetime.fromtimestamp(timestamp)
                    postTitle = title
                    postLink = ("https://www.reddit.com" + submission.permalink)
                    postUrl = (submission.url)
                    sendMessage(client, postTime, postTitle, postLink, postUrl)

def sendMessage(client, postTime, postTitle, postLink, postUrl):
    # Gather post content into list, probably can just do this in the monitorComments function when the variables are set
    messageBody = [postTime, postTitle, postLink, postUrl]
    # Formats and sends the message
    message = client.messages.create(
            body = (""" 
{}
{} 

{}

{}
""").format(messageBody[0], messageBody[1], messageBody[2], messageBody[3]),
            from_= config['twilio']['phoneNumber'],
            to = config['client']['phoneNumber']
        ) 
    # Append message details to log file
    with open('log.txt', 'a') as f:
        f.write(message + '\n')

try:
    # Runs entire program
    monitorComments(client, graphicsCard, processorUnit, monitor, subreddit)     

except KeyboardInterrupt:
    print("Ended")