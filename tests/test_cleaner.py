import unittest
from unittest import TestCase

import pandas as pd
from mynlpwrangler.cleaner import ArticleCleaner
import pandas.testing as pd_testing


class TestCleaner(TestCase):
    def setUp(self) -> None:
        self.data = {"id": ["10001", "11375", "23423"], "text": [
            "Hello, https://www.google.com/", "Hello,world", 'How do you do? http://www.google.com']}
        self._df = pd.DataFrame(self.data)
        self._ac = ArticleCleaner(col="text", cleaned_col="clean_text")
        self._clean_dict = {
            "id": ["10001", "11375", "23423"],
            "text": ["Hello, https://www.google.com/", "Hello,world", 'How do you do? http://www.google.com'],
            "clean_text": ["Hello ", "Hello world", "How do you do "]}
        self._clean_df = pd.DataFrame(self._clean_dict)

    def test_remove_url(self):
        text = self._ac.remove_url("Hello, https://www.google.com/")
        self.assertFalse(text)

    def test_remove_punctuation(self):
        rm_punt = self._ac.remove_punctuation("Hello,world")
        self.assertEqual(rm_punt, "Hello world")

    def test_set_clean_data(self):
        def clean_data_fun(df, col, new_col):
            df[new_col] = df[col].str.replace(" ", "")
            return df
        self._ac.set_clean_data(clean_data_fun)
        cleaned_data = self._ac.clean_data(self._df)
        self.assertEqual(
            cleaned_data['clean_text'].tolist(),
            ["Hello,https://www.google.com/", "Hello,world", "Howdoyoudo?http://www.google.com"])

    def test_clean_data(self):
        cleaned_data = self._ac.clean_data(self._df)
        self.assertIsInstance(cleaned_data, pd.DataFrame)
        pd_testing.assert_frame_equal(cleaned_data, self._clean_df)


if __name__ == "__main__":
    unittest.main()
