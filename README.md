pytwit
======

A twitter.com scraper

## Requirements

Run `pip install requests beautifulsoup4` to make sure you have all the requirements.

## Usage


### get_followers(username, delay = 1)

Gets followers of username
Inputs:Username, delay(optional, in seconds)
Outputs:list of username's followers

### get_following(username, delay = 1)

Gets list of who username is following
Inputs:Username, delay(optional, in seconds)
Outputs:list of who username is follwing

### get_bio(username)

Gets Twitter user's bio
Inputs: Username
Outputs: Bio

### get_tweets(username, limit = float("inf"), delay = 1)

Gets Twitter user's tweets
Inputs: username, number of pages of tweets to get (groups of 20), delay(optional, in seconds)
Outputs tweets

### get_tweet_data(username, id)

Gets extra data about a tweet
Inputs: username, tweet id
Outputs: Favorites, Retweets