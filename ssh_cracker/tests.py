from django.test import TestCase
from pexpect import pxssh
import os
# Create your tests here.

host=input()

with open('/var/python_test/test/django/web_security/static/dict/ssh_pwd.txt', 'r') as f:
    for line in f.readlines():
        line = line.strip('\n')
        user,passwd=line.split(':')

        try:
            s = pxssh.pxssh()
            s.login(host, user, passwd)
            print('mima'+user,passwd)
            break
        except Exception as e:
            print(e)
            continue

    print('fail')