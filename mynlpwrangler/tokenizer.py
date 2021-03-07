from typing import Callable

import jieba


class Tokenizer():
    def __init__(self, stop_word_path: str = None, token_function: Callable = None):
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
        for textword in seg_list.split('/'):
            if not (textword.strip() in stopwords_list) and len(textword.strip()) > 1:
                wordlist.append(textword)
        return ' '.join(wordlist)
