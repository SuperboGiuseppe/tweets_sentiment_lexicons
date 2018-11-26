# NLP Project

In this project you will study sentiment analysis of multi-lingual tweets and draw on conclusions whether each language brings distinct evidence regarding the 

## Requirement

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

```
MongoDB
Python environment
```

### Installing
1/ Install MongoDB
```
Download and install MongoDB Server here: https://www.mongodb.com/
```
2/ Install Python & setup environment
```
pip install requirement.txt
```
3/ Create folders
```
Create two folder data\db and tweets, run below command to change dbpath of MongoDB
mongod --dbpath <Absolute path of data\db>
```

### Run the project
## Get the tweet into database & histogram of languages distribution
* Import tweets from tweets.json into MongoDB with 
```
python insert_tweets.py
```
* Draw histogram:
```
python draw_bar_plot.py
```
## Translate non-English tweets into English

We use Yandex Translate API to translate tweets

```
python translate_tweets.py
```

## Use TweetTokenizer package to tokenize the tweet messages and remove all links and special characters, and draw histogram of the most common terms, excluding stop-words. 

```
---FILL HERE---
```

## Authors

-----FILL HERE-----

