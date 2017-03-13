#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


def print_usage():
    print ("Usage: migrate.py "
           "<csv-file-spendings> "
           "<csv-file-places> "
           "<sqlite-output-file>")


def read_csv_table(file_name):
    # TODO(f49dfdb9-1566-4edb-b60b-aede0d4d6f65): implement
    # read_csv_table()
    raise NotImplementedError


class SpendingsTable(object):
    def __init__(self, csv_table):
        self.csv_table = csv_table

    def dump(self, database):
        # TODO(fa4dd258-7ad9-4e58-9b23-5ea5f07d988c): implement
        # SpendingsTable.dump()
        raise NotImplementedError


class PlacesTable(object):
    def __init__(self, csv_table):
        self.csv_table = csv_table

    def dump(self, database):
        # TODO(c0c733e2-8fc2-4ce0-a0d1-bfcfa03eab8c): implement
        # PlacesTable.dump()
        raise NotImplementedError


class SqliteDatabase(object):
    def __init__(self, database_file_name):
        # TODO(d33be76e-b54d-42c2-91d7-c9a09b79ee0e): implement
        # SqliteDatabase constructor
        raise NotImplementedError

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_usage()
        exit(1)

    spendings_csv_table = read_csv_table(sys.argv[1])
    places_csv_table = read_csv_table(sys.argv[2])
    database = SqliteDatabase(sys.argv[3])

    SpendingsTable(spendings_csv_table).dump(database)
    PlacesTable(places_csv_table).dump(database)
