#!/usr/bin/env python
# -*- coding:utf-8 -*-
##################################
# logserver
# 通过socket接收并存储日志信息
# 注:测试程序为test_logserver.py
# 修改时间:2013-11-22
###################################

# standard lib
import os, sys
import time
import twisted
import logging
import traceback
import struct
import cPickle                 # use cPickle for speed
from logging.handlers import TimedRotatingFileHandler
from twisted.internet.protocol import Protocol, Factory

# our own code
import settings
from log_record import initlog

# 根据logger name生成一个
def gen_log_name(name):
    name = name.replace('.', '_')
    return name + '.log'

class ReceiveProtocol(Protocol):
    
    HEADER_LENGTH = 4
    def __init__(self):
        self.buf = ''
        self.state = 'init'
        self.require_length = ReceiveProtocol.HEADER_LENGTH
        # 记录当前完成初始化的logger名称
        self.logger_dict = {}
        
    def connectionMade(self):
        logger = logging.getLogger('log_server')
        logger.info('[makeConnection]与logger_client建立socket连接。')
        
    
    def dataReceived(self, data):
        logger = logging.getLogger('log_server')
        try:
            if len(self.buf + data) >= self.require_length:
                self.buf = self.buf + data
                # 数据就绪进行相应动作
                data = self.buf[0:self.require_length]
                # 把数据从缓冲区中取走
                self.buf = self.buf[self.require_length:]
                self.solve(data)
                # 可能一次读到了多条日志记录
                if self.buf:
                    self.dataReceived('')
            else:
                self.buf += data
                
        except BaseException, e:
            logger.error('处理短信记录失败' + str(e) + '\n' + traceback.format_exc())
            
    def solve(self, data):
        logger = logging.getLogger('log_server')
        statehandler = None
        try:
            pto = 'proto_' + self.state
            statehandler = getattr(self,pto)
        except AttributeError:
            logger.error('callback',self.state,'not found')
            self.transport.loseConnection()
        
        statehandler(data)
        if self.state == 'done':
            self.transport.loseConnection()
        
    def connectionLost(self, reason):
        logger = logging.getLogger('log_server')
        logger.info('[connectionLost]与logger_client的socket连接关闭。')
    
    
    # 记录日志
    def proto_record(self, data):
        logRecord = logging.makeLogRecord(cPickle.loads(data))
        if logRecord.name not in self.logger_dict:
            logger = initlog(logRecord.name, settings.PATH, gen_log_name(logRecord.name), logLevel=logging.DEBUG)
            self.logger_dict[logRecord.name] = logger
        
        self.logger_dict[logRecord.name].handle(logRecord)
            
        # 修改下一步动作以及所需长度
        self.state = 'init'
        self.require_length = ReceiveProtocol.HEADER_LENGTH
        
    # 处理头部信息
    def proto_init(self, data):
        length = struct.unpack('!I', data[0:ReceiveProtocol.HEADER_LENGTH])[0]
        
        # 修改下一步动作以及所需长度
        self.state = 'record'
        self.require_length = length
        
        if len(self.buf) >= self.require_length:
            data = self.buf[0:self.require_length]
            # 把数据从缓冲区中取走
            self.buf = self.buf[self.require_length:]
            self.solve(data)

        
class ReceiveFactory(Factory):
    def buildProtocol(self, addr):
        return ReceiveProtocol()

def main():
    print 'logserver has started.'
    logger = logging.getLogger('log_server')
    logger.info('logserver has started.')
     
    from twisted.internet import epollreactor
    epollreactor.install()
    reactor = twisted.internet.reactor
    reactor.listenTCP(settings.PORT, ReceiveFactory())
    reactor.run()
    

if __name__ == '__main__':
    main()
    
    
