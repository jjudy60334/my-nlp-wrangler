from urllib.parse import urlparse
import re
import string
import pandas as pd
import numpy as np
from typing import Callable


class ArticleCleaner():
    """
    clean data  for nlp
    """

    def __init__(self, col: str, cleaned_col: str = "clean_text"):
        self._col = col
        self._cleaned_col = cleaned_col
        self._clean_data_function = None

    def is_url(self, url: str):
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

    def set_clean_data(self, clean_data_fun: Callable):
        self._clean_data_function = clean_data_fun
        return self._clean_data_function

    def clean_data(self, df: pd.DataFrame, **kwargs):
        """
        for nlp clean data,it included remove url and puntuation
        """
        if not self._clean_data_function:
            df[self._col] = df[self._col].replace('\r', '', regex=True)
            df = df.dropna(subset=[self._col])
            df[self._cleaned_col] = [
                ' '.join(y for y in x.split() if not self.is_url(y)) for x in df[self._col]]
            df[self._cleaned_col] = df[self._cleaned_col].replace('\n', ' ', regex=True)
            df[self._cleaned_col] = df[self._cleaned_col].apply(self.remove_punctuation)
            df = df.replace(r'^\s*$', np.nan, regex=True)
            df = df.dropna(subset=[self._cleaned_col])
            df.drop_duplicates(subset=[self._cleaned_col], keep='last', inplace=True)
        else:
            self._clean_data_function(df, self._col, self._cleaned_col, **kwargs)
        return df
