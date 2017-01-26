from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import os,zipfile
# Create your views here.

def index(request):
    if request.method=='POST':
        file = request.FILES.get('upfile')
        if not file:
            return HttpResponse('no file upload ')
        des=open(os.path.join('/home/ttwilight',file.name),'wb+')
        for chunk in file.chunks():
            des.write(chunk)

        des.close()
        return HttpResponse('UP OK ')
    return render(request,'hacktools/index.html')

def extract_zip(path,pwd):
    zfile=zipfile.ZipFile(path)
    passwd=[]
    with open('/home/ttwilight/pwd.txt','r') as f :
        for line in f.readlines():
            passwd.append(line)

    for pwd in passwd:
        file = zfile.namelist()[0]
        pwd=pwd.strip('\n')
        pwd=bytes(pwd,encoding='utf-8')
        try:
            zfile.read(file,pwd=pwd)
            print('打开成功,压缩密码为',pwd)
            password = pwd
            break
        except:
            continue

    return password