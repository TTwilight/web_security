from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import os,zipfile
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    if request.method=='POST':
        file = request.FILES.get('upfile')
        if not file:
            return HttpResponse('no file upload ')
        zipname = file.name
        newfilename=os.path.join('/usr/zor_test/other',file.name)
        des=open(newfilename,'wb+')
        for chunk in file.chunks():
            des.write(chunk)
        des.close()
        # 实现上传后将文件分块写入服务器存储
        path=newfilename
        try:
            filelist,dirlist,password=extract_zip(path) #调用zip解压方法
            return render(request,'zip_decrypt/index.html',{'filelist':filelist,'dirlist':dirlist,'password':password,'zipname':zipname})
        except Exception as e:
            return HttpResponse(e)
        finally:
            os.system('rm -rf /usr/zor_test/other/*')
    return render(request,'zip_decrypt/index.html')

# zip解压解密方法
def extract_zip(path):
    zfile=zipfile.ZipFile(path)
    namelist=zfile.namelist()[1:]
    dirlist=[]
    filelist=[]
    for name in namelist:
        if name[-1:]=='/':
            dirlist.append(name)
        else:
            filelist.append(name)
    passwd=[]
    with open('static/dict/zip_pwd.txt','r') as f :  #服务器可以修改为绝对路径
        for line in f.readlines():
            passwd.append(str(line))

    for pwd in passwd:
        pwd=pwd.strip('\n')
        pwd=bytes(pwd,'utf-8')
        try:
            zfile.extractall(path='/usr/zor_test/other/',pwd=pwd)
            password = pwd
            zfile.close()
            return filelist,dirlist,password
        except:
            continue
    zfile.close()
    return filelist,dirlist,'尝试暴力破解失败'
