# -*- coding: utf-8 -*-
# @Time    : 2019/2/24 21:58
# @Author  : DELL
# @Email   : wayne_lau@aliyun.com
# @File    : run.py
# @Project : xiaoyou

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
# 导入flask项目
from main import app
#
# http_server = HTTPServer(WSGIContainer(app))
# http_server.listen(5000)  # 对应的flask端口
# IOLoop.instance().start()

# 开启多进程
http_server = HTTPServer(WSGIContainer(app))
http_server.bind(5000)
http_server.start(0)
IOLoop.instance().start()
