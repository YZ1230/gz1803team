#/user/bin/env/python
#-*- coding:utf-8 -*-
'''
author：baizhou
'''
from django.contrib.auth.backends import ModelBackend
from .models import MyUser


class MyBackends(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None

        try:
            user= MyUser.objects.get(username=username)
        except:
            try:
                user=MyUser.objects.get(phone=username)
            except:
                try:
                    user=MyUser.objects.get(email=username)
                except:
                    return None
        # print("********************************")
        if user.check_password(password):
            return user
        else:
            return None



