#!/usr/bin/env python
# V 1.1.5
import requests # For requesting URLs
import time # For processing time and sleep
from bs4 import BeautifulSoup # For searching HTML

#Gets usernames from twitter HTML
#Inputs:URL to scroll through
#Outputs:List of names(0),The "Show more" url(1)
def _usernames(url):
	# Step 1, find Usernames
	names = [] # Create names list
	r = requests.get(url) # Get url
	soup = BeautifulSoup(r.text) # Create bs4 object
	html = soup.select("td.info.fifty.screenname") # Find elements matching CSS
	soup = BeautifulSoup(str(html)) # Convert bs4 object back into HTML
	for link in soup.find_all('a',): # Find usernames
		name = link.get('name')
		if name:
			 names.append(name)
	# Step 2, Find link
	soup = BeautifulSoup(r.text) # Load the HTMl again to look for the link
	html = soup.select("div.w-button-more") # Find the "more" button with CSS
	soup = BeautifulSoup(str(html)) # Convert bs4 object back into HTML
	link = soup.find_all('a') #Determine of the link exists
	if link:
		nexturl = soup.find_all('a')[0].get("href") # Find the "more link"
	else:
		nexturl = False # Signal the end of the list
	output = [] # Create list for output
	output.insert(0, names) # List of usernames
	output.insert(1, nexturl) # "Show more" link
	return output

#Gets tweets from twitter HTML
#Inputs:URL to scroll through
#Outputs:List of tweets(0),The "Show more" url(1)
def _tweets(url):
	# Step 1, find Tweets
	tweets = [] # Create names list
	r = requests.get(url) # Get url
	soup = BeautifulSoup(r.text) # Create bs4 object
	html = soup.select(".ProfileTweet") # Find elements matching CSS
	count = 0 # Count for determining tweet in lilst
	for tweet in html:
		ctweet = [] # Current tweet
		ctweet.append(tweet.select(".ProfileTweet-screenname")[0].get_text().strip().replace('\n', '')) #Username
		ctweet.append(BeautifulSoup(str(tweet.select(".ProfileTweet-text")[0])).get_text().encode('ascii','ignore')) #Tweet text
		ctweet.append(BeautifulSoup(str(tweet.select('.ProfileTweet-timestamp')[0])).find_all('a')[0].get('href').split("/")[3].split("?")[0]) #Tweed id
		ctweet.append(time.strptime(tweet.select(".ProfileTweet-timestamp")[0].get('title'), "%I:%M %p - %d %b %Y")) #Date and time (as struct_time)
		count = count + 1
		tweets.append(ctweet)
	# Step 2, Find link
	soup = BeautifulSoup(r.text) # Load the HTMl again to look for the link
	bsnexturl = soup.select(".stream-container.persistent-inline-actions.light-inline-actions")
	if bsnexturl:
		nexturl = bsnexturl[0].get('data-max-id') # Find the "more" button with CSS
	else:
		nexturl = '-1'
	if nexturl == "-1":
		nexturl = False # Signal the end of the list
	output = [] # Create list for output
	output.append(tweets) # List of usernames
	output.append(nexturl) # "Show more" link
	return output

#Gets followers of username
#Inputs:Username, delay(optional, in seconds)
#Outputs:list of followers
def get_followers(username, delay = 1):
	url = "https://mobile.twitter.com/" + username + "/followers" # Set url of username
	_usernames_output = _usernames(url) # Get usernames on page 1
	followers = _usernames_output[0] # Start the followers
	while _usernames_output[1]: # While there are still more links
		url = "https://mobile.twitter.com" + _usernames_output[1]
		_usernames_output = _usernames(url)
		followers.extend(_usernames_output[0])
		time.sleep(delay)
	return followers # Return the list of followers
	
#Gets list of who username is following
#Inputs:Username, delay(optional, in seconds)
#Outputs:list of follwings
def get_following(username, delay = 1):
	url = "https://mobile.twitter.com/" + username + "/following" # Set url of username
	_usernames_output = _usernames(url) # Get usernames on page 1
	following = _usernames_output[0] # Start the followers
	while _usernames_output[1]: # While there are still more links
		url = "https://mobile.twitter.com" + _usernames_output[1]
		_usernames_output = _usernames(url)
		following.extend(_usernames_output[0])
		time.sleep(delay)
	return following # Return the list of followers
	
#Gets Twitter user's bio
#Inputs: Username
#Outputs: Bio
def get_bio(username):
	url = "https://mobile.twitter.com/" + username #set url
	r = requests.get(url) # Request HTML
	soup = BeautifulSoup(r.text) # Import HTML in HTML parser
	html = soup.select(".bio")# Select bio from CSS
	return BeautifulSoup(str(html[0])).get_text() # Extract Bio text
	
#Gets Twitter user's tweets
#Inputs: username, number of pages of tweets to get (groups of 20), delay(optional, in seconds)
#Outputs tweets, time
def get_tweets(username, limit = float("inf"), delay = 1):
	if limit == -1:
		limit = float("inf")
	url = "https://twitter.com/" + username #set url
	_tweets_output = _tweets(url) #Get list of tweets
	output = _tweets_output[0]
	count = 1
	while _tweets_output[1] and count < limit: # While there are still more links
		url = "https://twitter.com/" + username + "?max_id=" +  _tweets_output[1] # Set url from "show more" button
		_tweets_output = _tweets(url) #Request another page
		output.extend(_tweets_output[0])#Add the tweets
		count = count + 1
		time.sleep(delay)
	return output

#Gets extra data about a tweet
#Inputs: username, tweet id
#Outputs: Favorites, Retweets
def get_tweet_data(username, id):
	url = "https://twitter.com/" + username + "/status/" + id #setup url
	r = requests.get(url) # Request HTML
	soup = BeautifulSoup(r.text) # Import HTML into HTML parser
	html = soup.select(".request-retweeted-popup")#Select retweet number from HTML
	if html == []:
		rtweet = 0
	else:
		rtweet = int(BeautifulSoup(str(html[0])).get_text().replace(" ", "").replace("Retweets", "").replace("Retweet", "").replace("\n", ""))#Extract number of retweets
	html = soup.select(".request-favorited-popup")#Select favorites number from HTML
	if html == []:
		fav = 0
	else:
		fav = int(BeautifulSoup(str(html[0])).get_text().replace(" ", "").replace("Favorites", "").replace("Favorite", "").replace("\n", ""))#Extract number of favorites
	output = {}
	output['retweets'] = rtweet
	output['favorites'] = fav
	return output
