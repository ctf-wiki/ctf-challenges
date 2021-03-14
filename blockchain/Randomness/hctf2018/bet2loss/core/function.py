#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 1:32
# @Author  : LoRexxar
# @File    : function.py
# @Contact : lorexxar@gmail.com

import smtplib
import traceback
from random import Random

from bet2loss.settings import smtpport, smtpurl, emailpassword, emailuser


def random_str(size=8):
    str = ""
    chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    length = len(chars) - 1
    random = Random()

    for i in range(size):
        str += chars[random.randint(0, length)]
    return str


def random_num(start=2**20, end=2**30):
    random = Random()
    return random.randint(start,end)


try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(emailuser, emailpassword)

except:
    traceback.print_exc()
    print('smtp went wrong...')


def send_email(target_email, text):

    server.sendmail("lorexxar@gmail.com", target_email, text)
