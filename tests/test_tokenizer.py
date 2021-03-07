import unittest
import os
from unittest import TestCase
from mynlpwrangler.tokenizer import Tokenizer


class TestTokenizer(TestCase):
    def setUp(self) -> None:
        self.current_path = os.getcwd()
        self.stop_word_path = self.current_path + '/tests/data/stop_words.txt'
        self._tz = Tokenizer(stop_word_path=self.stop_word_path)
        self._text = "現在最流行的中文斷詞工具結巴(jieba)原本是以Python開發"

    def test_read_stop_words(self):
        stop_words = self._tz.read_stop_words()
        self.assertEqual(stop_words, ['1', '2', '4', 'hi'])

    def test_tokenize_text(self):
        tokenized_text = self._tz.tokenize_text(self._text)
        self.assertEqual(tokenized_text, "現在 流行 中文 斷詞 工具 結巴 jieba 原本 python 開發")


if __name__ == "__main__":
    unittest.main()