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
    with open('/home/ttwilight/pwd.txt') as f:
        for line in f.readlines():

            passwd.append(line)
    for pwd in passwd:
        file = zfile.namelist()[0]
        pwd=pwd.strip('\n')
        pwd=bytes(pwd,encoding='utf-8')
        try:
            text = zfile.read(file, pwd=pwd)
            print(str(text, encoding='utf-8'),'正确的密码为',pwd)
        except:
            continue




