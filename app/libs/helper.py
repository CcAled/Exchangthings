"""
@File  : helper.py
@Author: Zhourj
@Date  : 2019/12/26
@Desc  :
"""

__author__ = 'Zhourj'

def is_isbn_or_key(word):
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    short_word = word.replace('-', '')
    if '-' in word and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key
