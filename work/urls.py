#/user/bin/env/python
#-*- coding:utf-8 -*-
'''
author：baizhou
'''
from django.conf.urls import url

from .views import *
urlpatterns = [

    url(r'^get_verify_img', get_verify_img),
    url(r'^myregister$', my_register),
    url(r'^my_login$',my_login),
    url(r'^index$',index),
    url(r'^email/(.+)',active)

]
