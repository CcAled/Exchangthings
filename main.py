"""
@File  : main.py
@Author: Zhourj
@Date  : 2019/12/26
@Desc  :
"""

__author__ = 'Zhourj'

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'])
