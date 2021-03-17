import unittest
from unittest import TestCase
import os
from mynlpwrangler.tokenizer import Tokenizer
import pandas as pd


class TestTokenizer(TestCase):
    def setUp(self) -> None:
        self.current_path = os.getcwd()
        self.stop_word_path = self.current_path + '/tests/data/stop_words.txt'
        self._tz = Tokenizer(stop_word_path=self.stop_word_path)
        self._text = "現在最流行的中文斷詞工具結巴(jieba)原本是以Python開發"
        self._df = pd.DataFrame([self._text], columns=['text'])

    def test_read_stop_words(self):
        stop_words = self._tz.read_stop_words()
        self.assertEqual(stop_words, ['1', '2', '4', 'hi'])

    def test_tokenize_sentence(self):
        tokenized_text = self._tz.tokenize_sentence(self._text)
        self.assertEqual(tokenized_text, "現在 流行 中文 斷詞 工具 結巴 jieba 原本 python 開發")

    def test_set_tokenize_sentence(self):
        def tokenized_fun(setence):
            import monpa
            setence_list = monpa.cut(setence)
            setence_list.remove('jieba')
            return setence_list
        self._tz.set_tokenize_sentence(tokenized_fun)
        tokenized_text = self._tz.tokenize_sentence(self._text)
        self.assertEqual(tokenized_text, "現在 流行 中文 斷詞 工具 結巴 原本 python 開發")

    def test_tokenize_dataframe(self):
        tokenized_df = self._tz.tokenize_dataframe(self._df, sentences_column='text')
        self.assertEqual(tokenized_df['tokenized_word'].to_list()[0], "現在 流行 中文 斷詞 工具 結巴 jieba 原本 python 開發")


if __name__ == "__main__":
    unittest.main()
