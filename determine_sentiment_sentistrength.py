#!/usr/bin/python
# -*- encoding: utf-8 -*-

import csv
import mongodb_functions as mdb
from bson.objectid import ObjectId

def read_sentistrength_file(file_name, collection_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as result_file:
            reader = csv.reader(result_file, delimiter='\t')
            next(reader)

            collection = mdb.open_collection(collection_name, 'tweets')

            negative = 0
            positive = 0
            norm = 0
            count = 0
            id = ''

            for row in reader:
                positive = positive + int(row[2])
                negative = negative + int(row[3])
                norm = (int(row[2]) + int(row[3]))/4
                print(norm)
                id = row[0]
                collection.update({'_id': ObjectId(id)}, {'$set': {"SentiStrength": norm}})
                count = count + 1
            positive = positive / count
            negative = negative / count
            norm = norm / count
        result_file.close()
        return positive, negative, norm
    except FileNotFoundError as fnf:
        print(file_name, fnf.strerror)
        return -1, -1, -1


def main():
    pos_da, neg_da, norm_da = read_sentistrength_file('textfiles/tweets_da+results.txt', 'tweets_da')
    pos_en, neg_en, norm_en = read_sentistrength_file('textfiles/tweets_en+results.txt', 'tweets_en')
    pos_no, neg_no, norm_no = read_sentistrength_file('textfiles/tweets_no+results.txt', 'tweets_no')
    pos_fi, neg_fi, norm_fi = read_sentistrength_file('textfiles/tweets_fi+results.txt', 'tweets_fi')
    pos_sv, neg_sv, norm_sv = read_sentistrength_file('textfiles/tweets_sv+results.txt', 'tweets_sv')

    print("English:\nPositive: {}\tNegative: {}\tnormalized value: {}\n".format(pos_en, neg_en, norm_en))
    print("Finnish:\nPositive: {}\tNegative: {}\tnormalized value: {}\n".format(pos_fi, neg_fi, norm_fi))
    print("Danish:\nPositive: {}\tNegative: {}\tnormalized value: {}\n".format(pos_da, neg_da, norm_da))
    print("Norwegian:\nPositive: {}\tNegative: {}\tnormalized value: {}\n".format(pos_no, neg_no, norm_no))
    print("Swedish:\nPositive: {}\tNegative: {}\tnormalized value: {}\n".format(pos_sv, neg_sv, norm_sv))


if __name__ == "__main__": main()

