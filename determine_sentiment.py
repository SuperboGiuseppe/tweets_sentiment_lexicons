#!/usr/bin/python
# -*- encoding: utf-8 -*-

import csv


def read_sentistrength_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as result_file:
        reader = csv.reader(result_file, delimiter='\t')
        # headers = next(reader, None)
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


def main():
    pos, neg = read_sentistrength_file('/textfiles/placeholder_file.txt')
    print('Positive Value:')
    print(pos)
    print('Negative Value:')
    print(neg)


if __name__ == "__main__": main()
