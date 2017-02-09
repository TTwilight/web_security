from django.test import TestCase

# Create your tests here.
import zipfile,os
import optparse
from threading import Thread
from binascii import b2a_hex,a2b_hex,b2a_uu
path=input('请输入zip文件的路径：')

def extract_zip(pwd):
    pass

if os.path.exists(path):
    zfile=zipfile.ZipFile(path)
    passwd=[]
    with open('/usr/zor_test/dict/zip_pwd.txt') as f:
        for line in f.readlines():
            line.strip('\r\n')
            passwd.append(str(line))

    for pwd in passwd:
        file = zfile.namelist()[3]
        pwd=pwd.strip('\n')
        pwd=bytes(pwd,'utf-8')
        try:
            zfile.extractall(pwd=pwd)

            print('正确的密码为',pwd)
        except:
            continue






