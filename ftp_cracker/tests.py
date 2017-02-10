from django.test import TestCase
import ftplib
# Create your tests here.
host=input()
with open('/var/python_test/test/django/web_security/static/dict/ftp_pwd.txt', 'r') as f:
    for line in f.readlines():
        line = line.strip('\n')
        user, passwd = line.split(":")

        try:
            ftp = ftplib.FTP(host)
            ftp.login(user, passwd)
            ftp.quit()
            print('find'+user,passwd)
        except Exception as e:
            print(e)
            continue
    print('finis')