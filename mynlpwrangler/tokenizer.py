from typing import Callable

import jieba
import pandas as pd

class Tokenizer:
    def __init__(
            self, stop_word_path: str = None,
            token_function: Callable = None):
        """
        param:
        stop_word_path:the path of stop word
        sentences_column:name of columns which should be tokenized
        new_generate_column:name of new column

        """
        self._stop_word_path = stop_word_path
        self._token_function = token_function

    def read_stop_words(self):
        stopwords_list = []
        if self._stop_word_path:
            stopwords_list = [line.strip() for line in open(
                self._stop_word_path, 'r', encoding='UTF-8').readlines()]
        return stopwords_list

    def tokenize_text(self, text):
        text = text.lower()
        stopwords_list = self.read_stop_words()
        wordlist = []
        if self._token_function:
            seg_list = "/".join(self._token_function(text))
        else:
            seg_list = "/".join(jieba.cut(text, cut_all=False))
        for word in seg_list.split('/'):
            if not (word.strip() in stopwords_list) and len(word.strip()) > 1:
                wordlist.append(word)
        return ' '.join(wordlist)

    def tokenize_dataframe(self, df: pd.DataFrame, sentences_column: str = 'sentences',
                           new_generate_column: str = 'tokenized_word'):
        df[new_generate_column] = df[sentences_column].apply(self.tokenize_text)
        return df
