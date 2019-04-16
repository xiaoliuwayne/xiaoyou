# -*- coding: utf-8 -*-
# @Time    : 2018/12/25 15:55
# @Author  : DELL
# @Email   : wayne_lau@aliyun.com
# @File    : db.py
# @Project : MyServer

from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from config import conf
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
engine = create_engine(conf.POSTGRES_INFO, echo=True)
# 使用sessionmaker()不需要显式调用session.close()
Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=engine)
metadata = MetaData(bind=engine)
db_session = scoped_session(Session)
