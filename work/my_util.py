#/user/bin/env/python
#-*- coding:utf-8 -*-
'''
author：baizhou
'''

import random
import uuid
import hashlib
def get_random_color():
    R = random.randrange(255)
    G = random.randrange(255)
    B = random.randrange(255)
    return (R,G,B)


def get_random_str():
    uuid_val = uuid.uuid4()
    uuid_str = str(uuid).encode('utf-8')
    md5 = hashlib.md5()
    md5.update(uuid_str)
    return md5.hexdigest()


