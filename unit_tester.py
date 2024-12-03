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
        
        #make sure normalized.csv exists first, run python_analyzer.py to generate
        self.csv_file = './normalized.csv'

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

    def test_negative_values_exist_in_csv(self):
        # Load the CSV file into a DataFrame
        df = pd.read_csv(self.csv_file)

        # Ensure the columns of interest exist
        self.assertIn('killed', df.columns, "Column 'killed' not found in file")
        self.assertIn('injured', df.columns, "Column 'injured' not found in file")

        # Convert columns to numeric, coercing errors to NaN
        df['killed'] = pd.to_numeric(df['killed'], errors='coerce').fillna(0)
        df['injured'] = pd.to_numeric(df['injured'], errors='coerce').fillna(0)

        # Check for any negative values
        has_negative_killed = (df['killed'] < 0).any()
        has_negative_injured = (df['injured'] < 0).any()

        # Assert that no negative values exist
        self.assertFalse(
            has_negative_killed or has_negative_injured,
            "Negative values found in 'killed' or 'injured' columns"
        )
        
        
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

