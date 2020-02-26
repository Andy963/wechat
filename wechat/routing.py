#!usr/bin/env python
# *- coding:utf-8 -*-
# Author: Andy
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from api import consumers

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        url(r'^chat/$', consumers.ChatConsumer),
    ])
})