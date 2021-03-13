from urllib.parse import urlparse
import re
import string
import pandas as pd
import numpy as np


class ArticleCleaner():
    """
    clean data  for nlp
    """

    def __init__(self, df: pd.DataFrame, col: str, cleaned_col: str = "clean_text"):
        self._df = df
        self._col = col
        self._cleaned_col = cleaned_col

    def is_url(self, url):
        """
        remove the url from the post
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def remove_punctuation(self, line: str):
        """
        remove punctuation from the post
        """
        rule = re.compile("[^\u4e00-\u9fa5^.^a-z^A-Z]")
        line = rule.sub(' ', line)
        line = re.sub('[%s]' % re.escape(string.punctuation), '', line)
        return line

    def clean_data(self):
        """
        for nlp clean data,it included remove url and puntuation
        """
        self._df[self._col] = self._df[self._col].replace('\r', '', regex=True)
        self._df = self._df.dropna(subset=[self._col])
        self._df[self._cleaned_col] = [
            ' '.join(y for y in x.split() if not self.is_url(y)) for x in self._df[self._col]]
        self._df[self._cleaned_col] = self._df[self._cleaned_col].replace('\n', ' ', regex=True)
        self._df[self._cleaned_col] = self._df[self._cleaned_col].apply(self.remove_punctuation)
        self._df = self._df.replace(r'^\s*$', np.nan, regex=True)
        self._df = self._df.dropna(subset=[self._cleaned_col])
        self._df.drop_duplicates(subset=[self._cleaned_col], keep='last', inplace=True)
        return self._df
