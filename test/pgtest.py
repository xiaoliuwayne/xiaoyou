# -*- coding: utf-8 -*-
# @Time    : 2019/3/24 12:22
# @Author  : DELL
# @Email   : wayne_lau@aliyun.com
# @File    : pgtest.py
# @Project : xiaoyou

from common.db import db_session

sql = "select * from act_details"
result = db_session.execute(sql).fetchone()
for r in result:
    print 'r', r