#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from migrate import *


class TestMigrate(unittest.TestCase):
    def test_read_csv_table(self):
        csv_table = read_csv_table("test_csv_table")
        self.assertEqual(csv_table, [{'a': '10', 'b': '20'},
                                     {'a': '30', 'b': '40'}])

if __name__ == '__main__':
    unittest.main()
