#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import re
import sqlite3
from datetime import datetime


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
    m = re.match('<(\d{4})-(\d{2})-(\d{2}) ?\w*\.?(?: (\d{2}):(\d{2}))?>',
                 datestring,
                 re.UNICODE)
    (year, month, day, hours, minutes) = m.groups()

    if hours is None:
        hours = 0

    if minutes is None:
        minutes = 0

    return datetime(int(year), int(month), int(day), int(hours), int(minutes))


class ExpensesTable(object):
    def __init__(self, csv_table):
        self.records = [{'date': org2sqlite_date(row['date']),
                         'amount': int(float(row['amount']) * 100.00),
                         'name': row['name'],
                         'category': row['category'],
                         'place': row['place']}
                        for row in csv_table]

    def dump(self, database):
        for record in self.records:
            database.insert_into_table('Expenses', record)
        database.commit()


class PlacesTable(object):
    def __init__(self, csv_table):
        self.records = [{'codename': row['id'],
                         'address': row['address']}
                        for row in csv_table]

    def dump(self, database):
        for record in self.records:
            database.insert_into_table('Places', record)
        database.commit()


class SqliteDatabase(object):
    def __init__(self, database_connection):
        self.database_connection = database_connection

        schema_init_script = ('create table if not exists Places ('
                              '  id integer primary key,'
                              '  codename text not null,'
                              '  address text not null'
                              ');'
                              'create table if not exists Expenses ('
                              '  id integer primary key,'
                              '  date datetime not null,'
                              '  amount integer not null,'
                              '  name text not null,'
                              '  category text not null,'
                              '  place text'
                              ');')

        database_connection.executescript(schema_init_script)
        database_connection.commit()

    def insert_into_table(self, table_name, record):
        record_keys = record.keys()
        column_names = ', '.join(record_keys)
        column_values = ', '.join(map(lambda name: ':' + name,
                                      record_keys))
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name,
                                                     column_names,
                                                     column_values)

        self.database_connection.execute(query, record)

    def commit(self):
        self.database_connection.commit()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_usage()
        exit(1)

    expenses_csv_table = read_csv_table(sys.argv[1])
    places_csv_table = read_csv_table(sys.argv[2])
    database = SqliteDatabase(sqlite3.connect(sys.argv[3]))

    PlacesTable(places_csv_table).dump(database)
    ExpensesTable(expenses_csv_table).dump(database)
