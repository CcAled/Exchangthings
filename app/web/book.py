"""
 Created by 七月 on 2018-2-1.
"""
from flask import jsonify, request, current_app, url_for, render_template, flash
from flask_login import current_user

from app.forms.book import SearchForm
import json

from app.libs.helper import is_isbn_or_key
from app.spider.Things import Thing
from app.view_models.book import BookViewModel, BookCollection
from . import web

__author__ = '七月'

from ..models.gift import Gift

from ..models.wish import Wish
from ..view_models.trade import TradeInfo


@web.route('/book/search')
def search():
    """
        q :普通关键字 isbn
        page
        ?q=金庸&page=1
    """

    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        thing = Thing()

        if isbn_or_key == 'isbn':
            thing.search_by_isbn(q)
        else:
            thing.search_by_keyword(q, page)

        books.fill(thing, q)
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    thing = Thing()
    thing.search_by_isbn(isbn)

    if current_user.is_authenticated:
        # 如果未登录，current_user将是一个匿名用户对象
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    book = BookViewModel(thing.first)
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)

    return render_template('book_detail.html', book=book, has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model)
