# NLP Project
## Requirement

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Prerequisites

```
MongoDB
Python environment
```

## Installing
* Install MongoDB
```
Download and install MongoDB Server here: https://www.mongodb.com/
```
* Install Python & setup environment
```
pip install requirement.txt
```
* Create folders
```
Create two folder data\db and tweets, run below command to change dbpath of MongoDB
mongod --dbpath <Absolute path of data\db>
```

## Run the project
### Get the tweet into database & histogram of languages distribution
* Import tweets from tweets.json into MongoDB with 
```
python insert_tweets.py
```
* Draw histogram:
```
python draw_bar_plot.py
```
### Translate non-English tweets into English

We use Yandex Translate API to translate tweets

```
python translate_tweets.py
```

### Run the GUI 

```
In order to run the GUI, the mongodb framework must be launched previously with the correct db path.
"$python3 gui.py" inside the project directory.
```

## Authors
```
Emre Arkan
Katharina Geue
Giuseppe Superbo
Daniel Nguyen
Nicola Zotto
```

