#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from migrate import *


class SqliteDatabaseMock(object):
    def __init__(self):
        self.database = {}

    def insert_into_table(self, table_name, record):
        if table_name not in self.database:
            self.database[table_name] = []

        self.database[table_name].append(record)

    def assert_expected_records(self,
                                test_case,
                                table_name,
                                expected_records):
        test_case.assertEqual(self.database[table_name],
                              expected_records)


class TestMigrate(unittest.TestCase):
    def test_read_csv_table(self):
        csv_table = read_csv_table("test_csv_table")
        self.assertEqual(csv_table, [{'a': '10', 'b': '20'},
                                     {'a': '30', 'b': '40'}])

    def test_places_table(self):
        database = SqliteDatabaseMock()
        PlacesTable([{'id': 'foo',
                      'address': 'bar'},
                     {'id': 'hello',
                      'address': 'world'}]).dump(database)
        database.assert_expected_records(self, 'Places',
                                         [{'codename': 'foo',
                                           'address': 'bar'},
                                          {'codename': 'hello',
                                           'address': 'world'}])

if __name__ == '__main__':
    unittest.main()
