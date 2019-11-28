#!usr/bin/env python
# *- coding:utf-8 -*-
# Author: Andy
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer

CLIENT_LIST = []
class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        """ websocket连接到来时，自动执行 """
        print('有人来连接了')
        CLIENT_LIST.append(self)
        self.accept()

    def websocket_receive(self, message):
        """ websocket， 当浏览器给我发消息时，自动触发此方法 """
        print('接收到消息', message)
        # message是个字典
        for item in CLIENT_LIST:
            self.send(text_data='后台：收到了你的消息%s' % message['text'])

        # self.close() 主动关闭

    def websocket_disconnect(self, message):
        # 如果浏览器断开了连接，这个方法被触发
        CLIENT_LIST.remove(self)
        print('客户端主动断开连接了')
        # 浏览器断开了，我也要断开，规定我要断开抛出下面的异常
        raise StopConsumer()
