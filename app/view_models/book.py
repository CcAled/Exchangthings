"""
@File  : book.py
@Author: Zhourj
@Date  : 2019/12/27
@Desc  :
"""

__author__ = 'Zhourj'


class BookViewModel:
    def __init__(self, data):
        self.title = data['title']
        self.publisher = data['publisher']
        self.author = '、'.join(data['author'])
        self.image = data['image']
        self.price = '￥' + data['price'] if data['price'] else data['price']
        self.summary = data['summary']
        self.isbn = data['isbn']
        self.pubdate = data['pubdate']
        self.summary = data['summary']
        self.pages = data['pages']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return '/'.join(intros)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = None

    def fill(self, things, keyword):
        self.total = things.total
        self.books = [BookViewModel(book) for book in things.books]
        self.keyword = keyword
