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


# TODO(0aa53ea3-793f-4a1a-ac88-7fd0e5311cf8): Split TestMigrate
#
# We need to simply split it by classes and methods.
# https://docs.python.org/2/library/unittest.html
class TestMigrate(unittest.TestCase):
    # TODO(97c029b0-4d91-4784-855d-dd69a07278fe): create
    # test_csv_table file in tempdir before the test
    def test_read_csv_table(self):
        csv_table = read_csv_table("test_csv_table")
        self.assertEqual(csv_table, [{u'a': u'10',
                                      u'b': u'20',
                                      u'ы': u'привет'},
                                     {u'a': u'30',
                                      u'b': u'40',
                                      u'ы': u'мир'}])

    def test_places_table(self):
        database = SqliteDatabaseMock()
        PlacesTable([{'id': u'foo',
                      'address': u'bar'},
                     {'id': u'hello',
                      'address': u'world'}]).dump(database)
        database.assert_expected_records(self, 'Places',
                                         [{'codename': u'foo',
                                           'address': u'bar'},
                                          {'codename': u'hello',
                                           'address': u'world'}])

    def test_org2sqlite_date(self):
        self.assertEqual(org2sqlite_date(u"<2016-06-07 Tue>"),
                         u"datetime('2016-06-07')")
        self.assertEqual(org2sqlite_date(u"<2016-06-58 Привет>"),
                         u"datetime('2016-06-58')")
        self.assertEqual(org2sqlite_date(u"<2016-06-58 Мир.>"),
                         u"datetime('2016-06-58')")
        self.assertEqual(org2sqlite_date(u"<2016-06-06 Mon 12:60>"),
                         u"datetime('2016-06-06 12:60')")

    def test_expenses_table(self):
        database = SqliteDatabaseMock()
        ExpensesTable([{'date': u'<2016-06-07 Tue>',
                        'amount': u'-105.00',
                        'name': u'Hello',
                        'category': u'misc',
                        'place': u''},
                       {'date': u'<2016-06-07 Tue 12:50>',
                        'amount': u'-0.0',
                        'name': u'Привет',
                        'category': u'food',
                        'place': u'foo'},
                       {'date': u'<2016-06-09 Чт. 12:39>',
                        'amount': u'-1000.00',
                        'name': u'Hello Мир',
                        'category': u'communications',
                        'place': u'test'}]).dump(database)

        expected_records = [{"date": u"datetime('2016-06-07')",
                             "amount": u"-105.00",
                             "name": u"Hello",
                             "category": u"misc",
                             "place": u""},
                            {"date": u"datetime('2016-06-07 12:50')",
                             "amount": u"-0.0",
                             "name": u"Привет",
                             "category": u"food",
                             "place": u"foo"},
                            {"date": u"datetime('2016-06-09 12:39')",
                             "amount": u"-1000.00",
                             "name": u"Hello Мир",
                             "category": u"communications",
                             "place": u"test"}]

        database.assert_expected_records(self, 'Expenses', expected_records)


class SqliteConnectionMock(object):
    def __init__(self):
        self.queries = []

    def execute(self, query, parameters={}):
        self.queries.append((query, parameters))

    def assert_expected_queries(self, test_case, expected_queries):
        test_case.assertEqual(self.queries, expected_queries)


class SqliteDatabaseTest(unittest.TestCase):
    def test_insert_into_table(self):
        connection = SqliteConnectionMock()
        database = SqliteDatabase(connection)

        database.insert_into_table('Hello', {'number': '1',
                                             'name': 'Foo'})
        database.insert_into_table('Hello', {'number': '2',
                                             'name': 'Bar'})
        database.insert_into_table('World', {'a': 'b',
                                             'c': 'd'})

        expected_queries = [('INSERT INTO Hello '
                             '(number, name) '
                             'VALUES (:number, :name)',
                             {'number': '1',
                              'name': 'Foo'}),
                            ('INSERT INTO '
                             'Hello (number, name) '
                             'VALUES (:number, :name)',
                             {'number': '2',
                              'name': 'Bar'}),
                            ('INSERT INTO '
                             'World (a, c) '
                             'VALUES (:a, :c)',
                             {'a': 'b',
                              'c': 'd'})]

        connection.assert_expected_queries(self, expected_queries)


if __name__ == '__main__':
    unittest.main()
