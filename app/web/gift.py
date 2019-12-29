from flask import current_app, flash, url_for, redirect, render_template
from flask_login import login_required, current_user
from sqlalchemy import desc

from . import web

__author__ = '七月'

from .. import db

from ..models.gift import Gift
from ..view_models.gift import MyGifts


@web.route('/my/gifts')
@login_required
def my_gifts():
    # uid = current_user.id
    # gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
    #     desc(Gift.create_time)).all()
    # wishes_count = GiftService.get_wish_counts(gifts)
    # view_model = MyGifts(gifts, wishes_count).package()
    # return render_template('my_gifts.html', gifts=view_model)
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_count(isbn_list)
    view_model = MyGifts(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.my_gifts)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        flash('这本书已添加或存在于你的愿望清单中')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass
