#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv


def print_usage():
    print ("Usage: migrate.py "
           "<csv-file-expenses> "
           "<csv-file-places> "
           "<sqlite-output-file>")


def read_csv_table(file_name):
    with open(file_name, 'rb') as csvfile:
        csvreader = csv.DictReader(csvfile)
        return [row for row in csvreader]


def org2sqlite_date(datestring):
    # TODO(43d4478b-72f0-4eb0-af7e-875fc4a887f4): implement org2sqlite_date
    #
    # Split from fa4dd258-7ad9-4e58-9b23-5ea5f07d988c
    raise NotImplementedError


# TODO(fa4dd258-7ad9-4e58-9b23-5ea5f07d988c): implement ExpensesTable
#
# Pieces:
# - 43d4478b-72f0-4eb0-af7e-875fc4a887f4
class ExpensesTable(object):
    def __init__(self, csv_table):
        self.records = [{'date': org2sqlite_date(row['date']),
                         'amount': row['amount'],
                         'name': row['name'],
                         'category': row['category'],
                         'place': row['place']}
                        for row in csv_table]

    def dump(self, database):
        for record in self.records:
            database.insert_into_table('Expenses', record)


class PlacesTable(object):
    def __init__(self, csv_table):
        self.records = [{'codename': row['id'],
                         'address': row['address']}
                        for row in csv_table]

    def dump(self, database):
        for record in self.records:
            database.insert_into_table('Places', record)


class SqliteDatabase(object):
    def __init__(self, database_file_name):
        # TODO(d33be76e-b54d-42c2-91d7-c9a09b79ee0e): implement
        # SqliteDatabase constructor
        raise NotImplementedError

    def insert_into_table(self, table_name, record):
        # TODO(ca10aaa6-b33c-4b44-b273-c136bd98247d): implement
        # SqliteDatabase.insert_into_table()
        raise NotImplementedError

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_usage()
        exit(1)

    expenses_csv_table = read_csv_table(sys.argv[1])
    places_csv_table = read_csv_table(sys.argv[2])
    database = SqliteDatabase(sys.argv[3])

    PlacesTable(places_csv_table).dump(database)
    ExpensesTable(expenses_csv_table).dump(database)
