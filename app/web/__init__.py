"""
@File  : __init__.py
@Author: Zhourj
@Date  : 2019/12/26
@Desc  :
"""

__author__ = 'Zhourj'

from flask import Blueprint

web = Blueprint('web', __name__)

from app.web import auth
from app.web import main
from app.web import book
from app.web import wish
from app.web import gift
from app.web import drift