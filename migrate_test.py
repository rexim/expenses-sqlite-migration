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

    @unittest.skip('Waiting for 43d4478b-72f0-4eb0-af7e-875fc4a887f4')
    def test_expenses_table(self):
        database = SqliteDatabaseMock()
        ExpensesTable([{'date': '<2016-06-07 Tue>',
                        'amount': '-105.00',
                        'name': 'Hello',
                        'category': 'misc',
                        'place': ''},
                       {'date': '<2016-06-07 Tue 12:50>',
                        'amount': '-0.0',
                        'name': 'Привет',
                        'category': 'food',
                        'place': 'foo'},
                       {'date': '<2016-06-09 Чт. 12:39>',
                        'amount': '-1000.00',
                        'name': 'Hello Мир',
                        'category': 'communications',
                        'place': 'test'}]).dump(database)

        expected_records = [{"date": "datetime('2016-06-07')",
                             "amount": "-105.00",
                             "name": "Hello",
                             "category": "misc",
                             "place": ""},
                            {"date": "datetime('2016-06-07 12:50')",
                             "amount": "-0.0",
                             "name": "Привет",
                             "category": "food",
                             "place": "foo"},
                            {"date": "datetime('2016-06-09 12:39')",
                             "amount": "-1000.00",
                             "name": "Hello Мир",
                             "category": "communications",
                             "place": "test"}]

        database.assert_expected_records(self, 'Expenses', expected_records)

if __name__ == '__main__':
    unittest.main()
