#!usr/bin/env python
# *- coding:utf-8 -*-
# Author: Andy
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


# CLIENT_LIST = []
class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        """ websocket连接到来时，自动执行 """
        print('有人来连接了')
        async_to_sync(self.channel_layer.group_add)('111', self.channel_name)  # 加到一群，self.channel)name为随机id
        # 111 为group name 不要用中文，"Group name not valid
        # CLIENT_LIST.append(self)
        self.accept()

    def websocket_receive(self, message):
        """ websocket， 当浏览器给我发消息时，自动触发此方法 """
        print('接收到消息', message)
        # message是个字典
        # for item in CLIENT_LIST:
        #     self.send(text_data='后台：收到了你的消息%s' % message['text'])
        # 给一群所有人发信息
        async_to_sync(self.channel_layer.group_send)('111', {
            'type': 'callback.func',  # 类似回调函数，通过下面的callback_fun, 这里应该是用点，在channels内部会将点换成下划线
            'message': message['text']
        })

        # self.close() 主动关闭, 发过来的event是个字典，

    def callback_func(self, event):
        message = event['message']
        self.send(message)

    def websocket_disconnect(self, message):
        # 如果浏览器断开了连接，这个方法被触发
        # CLIENT_LIST.remove(self)
        async_to_sync(self.channel_layer.group_discard)('111', self.channel_name)
        print('客户端主动断开连接了')
        # 浏览器断开了，我也要断开，规定我要断开抛出下面的异常
        raise StopConsumer()
