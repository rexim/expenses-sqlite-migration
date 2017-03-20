#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import re
import sqlite3


def print_usage():
    print ("Usage: migrate.py "
           "<csv-file-expenses> "
           "<csv-file-places> "
           "<sqlite-output-file>")


def read_csv_table(file_name):
    with open(file_name, 'rb') as csvfile:
        csvreader = csv.DictReader(csvfile)
        return [{unicode(k, 'utf-8'): unicode(v, 'utf-8')
                 for k, v in row.iteritems()}
                for row in csvreader]


# TODO(c3ee0412-31c7-4d7d-bd86-36ff23045542): move org2sqlite_date
# inside of ExpensesTable
def org2sqlite_date(datestring):
    m = re.match('<(\d{4}-\d{2}-\d{2}) ?\w*\.?( \d{2}:\d{2})?>',
                 datestring,
                 re.UNICODE)
    (d, t) = m.groups()

    if t is None:
        t = ''

    return "datetime('%s%s')" % (d, t)


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
    def __init__(self, database_connection):
        self.database_connection = database_connection

    def insert_into_table(self, table_name, record):
        column_names = ', '.join(record.keys())
        column_values = ', '.join(map(lambda name: ':' + name,
                                      record.keys()))
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name,
                                                     column_names,
                                                     column_values)

        self.database_connection.execute(query, record)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_usage()
        exit(1)

    expenses_csv_table = read_csv_table(sys.argv[1])
    places_csv_table = read_csv_table(sys.argv[2])
    database = SqliteDatabase(sqlite3.connect(sys.argv[3]))

    PlacesTable(places_csv_table).dump(database)
    ExpensesTable(expenses_csv_table).dump(database)
