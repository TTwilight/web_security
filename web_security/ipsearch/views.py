from django.shortcuts import render
from django.http import HttpResponse,Http404
from urllib.request import urlopen,urlretrieve
from bs4 import BeautifulSoup
import json
import os
from binascii import a2b_hex,b2a_hex
# Create your views here.

def index(request):
    ipaddress=request.POST.get('ipadd')
    b=isinstance(ipaddress,str)
    if os.path.exists('/var/python_test/test/django/web_security/web_security/ipsearch/static/ipsearch/test.jpg'):
        os.remove('/var/python_test/test/django/web_security/web_security/ipsearch/static/ipsearch/test.jpg')
    if ipaddress:
        a='http://freegeoip.net/json/'+ipaddress
        html=urlopen(a)
        hjson=json.loads(html.read().decode('utf-8'))
        longitude=str(hjson['longitude'])
        latitude=str(hjson['latitude'])
        baiduapi='http://api.map.baidu.com/staticimage/v2?ak=hNFf8i21Y8lPPlNbMXvt247DCIrtbDIR&center='+longitude+','+latitude+'&width=400&height=400&zoom=12'
        path='/var/python_test/test/django/web_security/web_security/ipsearch/static/ipsearch/'+'test.jpg'
        urlretrieve(baiduapi,path)
    return render(request,'ipsearch/index.html',{'ipadd':ipaddress})