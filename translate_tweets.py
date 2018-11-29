import pymongo
from yandex_translate import YandexTranslate


def translate_tweets(text):
    translate = YandexTranslate("trnsl.1.1.20181124T190331Z.a0bc7666f73f538b.c226a7ab6967c717853213c927d86dd6b63e6bd9")
    return translate.translate(text, 'en')["text"][0]


def translate_database(db_name='tweets'):
    connection = pymongo.MongoClient("mongodb://localhost:20000")
    db = connection[db_name]
    tweets_da = db['tweets_da']
    tweets_fi = db['tweets_fi']
    tweets_no = db['tweets_no']
    tweets_sv = db['tweets_sv']
    try:
        # Translate tweet - English
        for tweet in tweets_da.find():
            tweets_da.update({"_id": tweet["_id"]}, {'$set': {"translated_text": translate_tweets(tweet["text"])}})
        print("Tweets DA translated")
        for tweet in tweets_fi.find():
            tweets_fi.update({"_id": tweet["_id"]}, {'$set': {"translated_text": translate_tweets(tweet["text"])}})
        print("Tweets FI translated")
        for tweet in tweets_no.find():
            tweets_no.update({"_id": tweet["_id"]}, {'$set': {"translated_text": translate_tweets(tweet["text"])}})
        print("Tweets NO translated")
        for tweet in tweets_sv.find():
            tweets_sv.update({"_id": tweet["_id"]}, {'$set': {"translated_text": translate_tweets(tweet["text"])}})
        print("Tweets SV translated")
    except ValueError:
        print(ValueError)


if __name__ == '__main__':
    translate_database()
