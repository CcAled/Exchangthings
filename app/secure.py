"""
@File  : secure.py
@Author: Zhourj
@Date  : 2019/12/26
@Desc  :
"""

__author__ = 'Zhourj'

SECRET_KEY = '\x88D\xf09\x91\x07\x98\x89\x87\x96\xa0A\xc68\xf9\xecJ:U\x17\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x98*4'


DEBUG = False
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://zhou:zhou@121.36.24.124:3306/ChangeThings'
#解决warning
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_TEARDOWN = True


# Email 配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = '342928796@qq.com'
MAIL_PASSWORD = 'abjjytmbmrkwbhjh'
MAIL_SUBJECT_PREFIX = '[易物]'
MAIL_SENDER = '易物 <342928796@qq.com>'


