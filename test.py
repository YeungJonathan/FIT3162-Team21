import unittest
import pandas as pd
from main import missing_values_table


class missing_values_testcase(unittest.TestCase):
    """test function missing_values_table"""

    def test_missing_values_1(self):
        """return correct table"""
        test = pd.read_excel('test_missing_value.xlsx')
        table = missing_values_table(test)
        self.assertEqual(table['Missing Values'][0.8], 8)

    def test_missing_values_2(self):
        """return correct table"""
        test = pd.read_excel('test_missing_value.xlsx')
        table = missing_values_table(test)
        self.assertEqual(table['% of Total Values'][0.3], 30)

    def test_missing_values_3(self):
        """return correct table"""
        test = pd.read_excel('test_missing_value.xlsx')
        table = missing_values_table(test)
        self.assertEqual(table['Missing Values'][0.5], 5)

    def test_missing_values_4(self):
        """return correct table"""
        test = pd.read_excel('test_missing_value.xlsx')
        table = missing_values_table(test)
        self.assertEqual(table['% of Total Values'][0.5], 50)


