import unittest
import pandas as pd
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestDay1Data(unittest.TestCase):

    def setUp(self):
        self.data_path = 'dataset/partners.csv'

    def test_partners_file_exists(self):
        """Check if partners.csv exists"""
        self.assertTrue(os.path.exists(self.data_path), f"File not found: {self.data_path}")
        
    def test_partners_data_shape(self):
        """Check if data has rows and columns"""
        if os.path.exists(self.data_path):
            df = pd.read_csv(self.data_path)
            self.assertFalse(df.empty, "Dataset is empty")
            self.assertGreater(len(df.columns), 5, "Dataset has too few columns")
            
    def test_churn_label_exists(self):
        """Ensure target variable exists"""
        if os.path.exists(self.data_path):
            df = pd.read_csv(self.data_path)
            self.assertIn('churn_label', df.columns, "Target column 'churn_label' missing")

if __name__ == '__main__':
    unittest.main()
