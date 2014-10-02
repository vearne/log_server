#!/usr/bin/env python
# -*- coding:utf-8 -*-
##################################
# logserver 配置文件
# 修改时间:2013-11-22
###################################
import logging
from log_record import initlog


PORT = 9030

# 日志文件存储路径
PATH = "/tmp"

# 日志记录
initlog('log_server', PATH, 'log_server.log', logging.INFO)


