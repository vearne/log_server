# -*- coding:utf-8 -*-                                                                                                                                                  
import logging
import os
from logging.handlers import TimedRotatingFileHandler

def initlog(logger_name, logpath, filename, logLevel=logging.INFO):
    if logger_name not in logging.Logger.manager.loggerDict:
        logfile = os.path.join(logpath, filename)
        logger = logging.getLogger(logger_name)
        # 默认 每天24:00会对日志进行归档,最多保留7天的日志
        handler = TimedRotatingFileHandler(logfile, when='midnight',backupCount=7)
        datefmt = "%Y-%m-%d %H:%M:%S"
        format_str = "[%(asctime)s]: %(name)s %(levelname)s %(lineno)s %(message)s"
        formatter = logging.Formatter(format_str, datefmt)
        handler.setFormatter(formatter)
        handler.setLevel(logLevel)
        logger.addHandler(handler)
        logger.setLevel(logLevel)
        
    return logging.getLogger(logger_name)
