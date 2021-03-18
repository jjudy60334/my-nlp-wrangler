# MyNLPWrangler

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
## Description
This is a framwork for nlp clean data wrangler


## Flow
## Cleaner
- remove puncuation
- remove rul

## Tokenizer
- default by jeiba tokenizer 
- remove stop words 

## Quick Start
Installation command: `pip install my-nlp-wrangler`

```py3
from mynlpwrangler.cleaner import ArticleCleaner
from mynlpwrangler.tokenizer import Tokenizer

df = pd.DataFrame(
    {
    "id": ["10001", "11375", "23423"],
    "text": ["Hello, https://www.google.com/", "Hello,world", 'How do you do? http://www.google.com']
    })

# To clean the sentence by removing the puncuation and url
ac = ArticleCleaner(col='content',cleaned_col='clean_sentence')
clean_data = ac.clean_data(df=article_df)

# Tokentize the sentence and generate the segmented word
tokenized_column = 'tokenize_word'
tk=Tokenizer(stop_word_path = f'{os.getcwd()}/stop_word.txt')
tk.tokenize_dataframe(clean_data,sentences_column = 'content',new_generate_column = tokenized_column)