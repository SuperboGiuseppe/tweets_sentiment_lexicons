#!/usr/bin/python
# -*- encoding: utf-8 -*-

import csv


def read_sentistrength_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as result_file:
            reader = csv.reader(result_file, delimiter='\t')
            next(reader)
            negative = 0
            positive = 0
            count = 0
            for row in reader:
                positive = positive + int(row[2])
                negative = negative + int(row[3])
                count = count + 1
            positive = positive / count
            negative = negative / count
        result_file.close()
        return positive, negative
    except FileNotFoundError as fnf:
        print(file_name, fnf.strerror)
        return -1, -1


def main():
    pos_da, neg_da = read_sentistrength_file('textfiles/tweets_da+results.txt')
    pos_en, neg_en = read_sentistrength_file('textfiles/tweets_en+results.txt')
    pos_no, neg_no = read_sentistrength_file('textfiles/tweets_no+results.txt')
    pos_fi, neg_fi = read_sentistrength_file('textfiles/tweets_fi+results.txt')
    pos_sv, neg_sv = read_sentistrength_file('textfiles/tweets_sv+results.txt')

    print("English:\nPositive: {}\tNegative: {}\tGeneral: {}\n".format(pos_en, neg_en, pos_en+neg_en))
    print("Finnish:\nPositive: {}\tNegative: {}\tGeneral: {}\n".format(pos_fi, neg_fi, pos_fi+neg_fi))
    print("Danish:\nPositive: {}\tNegative: {}\tGeneral: {}\n".format(pos_da, neg_da, pos_da+neg_da))
    print("Norwegian:\nPositive: {}\tNegative: {}\tGeneral: {}\n".format(pos_no, neg_no, pos_no+neg_no))
    print("Swedish:\nPositive: {}\tNegative: {}\tGeneral: {}\n".format(pos_sv, neg_sv, pos_sv+neg_sv))


if __name__ == "__main__": main()

