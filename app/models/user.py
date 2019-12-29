from flask import current_app
from flask_login import UserMixin, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.enums import PendingStatus
from app.models.drift import Drift
from app.models.gift import Gift
from app.libs.helper import is_isbn_or_key

__author__ = 'bliss'

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy import String, Unicode, DateTime, Boolean
from sqlalchemy import SmallInteger, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import Base, db
from app.models.wish import Wish
from app.spider.Things import Thing


class User(UserMixin, Base):
    __tablename__ = 'user'
    # __bind_key__ = 'fisher'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    gifts = relationship('Gift')
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))
    _password = Column('password', String(100), nullable=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    def can_satisfied_wish(self, current_gift_id=None):
        if current_gift_id:
            gift = Gift.query.get(current_gift_id)
            if gift.uid == self.id:
                return False
        if self.beans < 1:
            return False
        success_gifts = Drift.query.filter(Drift.pending == PendingStatus.success,
                                           Gift.uid == self.id).count()
        success_receive = Drift.query.filter(Drift.pending == PendingStatus.success,
                                             Drift.requester_id == self.id).count()
        return False if success_gifts <= success_receive - 2 else True

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        thing = Thing()
        thing.search_by_isbn(isbn)
        if not thing.first:
            return False
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('id'))
        if user is None:
            return False
        user.password = new_password
        db.session.commit()
        return True

