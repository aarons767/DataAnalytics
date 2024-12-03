import unittest
import pandas as pd
from scipy import stats
from datetime import datetime
import numpy as np


class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        # Sample data to mimic the dataset
        self.data = pd.DataFrame({
            'incident_date': ['January 1 2020', 'February 15 2020', 'March 10 2020'],
            'killed': ['1', '2', 'invalid'],
            'injured': ['3', 'invalid', '5']
        })

    def test_convert_date(self):
        # Test the date conversion function
        def convert_date(this_date):
            try:
                return datetime.strptime(this_date, '%B %d %Y').strftime('%m-%d-%Y')
            except ValueError:
                return this_date

        self.data['incident_date'] = self.data['incident_date'].apply(convert_date)
        expected_dates = ['01-01-2020', '02-15-2020', '03-10-2020']
        self.assertListEqual(self.data['incident_date'].tolist(), expected_dates)

    def test_numeric_conversion(self):
        # Test conversion of 'killed' and 'injured' columns to numeric
        self.data['killed'] = pd.to_numeric(self.data['killed'], errors='coerce').fillna(0)
        self.data['injured'] = pd.to_numeric(self.data['injured'], errors='coerce').fillna(0)

        expected_killed = [1.0, 2.0, 0.0]
        expected_injured = [3.0, 0.0, 5.0]

        self.assertListEqual(self.data['killed'].tolist(), expected_killed)
        self.assertListEqual(self.data['injured'].tolist(), expected_injured)

    def test_filter_outliers(self):
        # Test filtering out rows where 'killed' or 'injured' > 50
        self.data['killed'] = pd.to_numeric(self.data['killed'], errors='coerce').fillna(0)
        self.data['injured'] = pd.to_numeric(self.data['injured'], errors='coerce').fillna(0)

        filtered_data = self.data[(self.data['killed'] <= 50) & (self.data['injured'] <= 50)]

        # Since no values are > 50, same as the original
        self.assertEqual(len(filtered_data), len(self.data))

    def test_statistics(self):
        self.data['killed'] = pd.to_numeric(self.data['killed'], errors='coerce').fillna(0)
        self.data['injured'] = pd.to_numeric(self.data['injured'], errors='coerce').fillna(0)

        mean_killed = self.data['killed'].mean()
        median_killed = self.data['killed'].median()
        mode_killed = stats.mode(self.data['killed'], keepdims=True).mode[0]
        std_killed = self.data['killed'].std()

        self.assertAlmostEqual(mean_killed, 1.0)
        self.assertAlmostEqual(median_killed, 1.0)
        self.assertEqual(mode_killed, 0.0)
        self.assertAlmostEqual(std_killed, 1.0)

    def test_outliers(self):
        self.data['killed'] = pd.to_numeric(self.data['killed'], errors='coerce').fillna(0)
        self.data['injured'] = pd.to_numeric(self.data['injured'], errors='coerce').fillna(0)

        outliers = self.data[(self.data['killed'] > 50) | (self.data['injured'] > 50)]

        self.assertTrue(outliers.empty)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)

