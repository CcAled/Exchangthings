"""
@File  : https.py
@Author: Zhourj
@Date  : 2019/12/26
@Desc  :
"""

__author__ = 'Zhourj'

import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else r.text
        return r.json() if return_json else r.text
