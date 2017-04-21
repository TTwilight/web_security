from django.shortcuts import render
from django.http import HttpResponse,Http404
from urllib.request import urlopen,urlretrieve,Request
import nmap
import json
import os
from binascii import a2b_hex,b2a_hex
from django.contrib.auth.decorators import login_required

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
@login_required
def index(request):
    ipaddress=request.POST.get('ipadd')

    if os.path.exists(os.path.join(BASE_DIR,'ipsearch/static/ipsearch/test.jpg')):    #apache 中会找不到app的静态文件，需要使用python manage.py collectstatic 将其收集到根目录static文件下,
        os.remove(os.path.join(BASE_DIR,'ipsearch/static/ipsearch/test.jpg'))         #然后配置/etc/apache2/sites-available里conf 文件,另外需要将此出以及path处的ipsearch/static/ipsearch/test.jpg
                                                                                      #换成  static/ipsearch/test.jpg
    if ipaddress:
        ipaddress=ipaddress.strip()
        try:
            a='http://freegeoip.net/json/'+ipaddress
            html=urlopen(a)
            hjson=json.loads(html.read().decode('utf-8'))
            longitude=str(hjson['longitude'])
            latitude=str(hjson['latitude'])
            country=str(hjson['country_name'])
            address=str(hjson['region_name'])+' '+str(hjson['city'])
            time_zone=str(hjson['time_zone'])
            baiduapi='http://api.map.baidu.com/staticimage/v2?ak=hNFf8i21Y8lPPlNbMXvt247DCIrtbDIR&center='+longitude+','+latitude+'&width=400&height=400&zoom=12'
            path=os.path.join(BASE_DIR,'ipsearch/static/ipsearch/')+'test.jpg'     #部署注意修改文件权限，不然不能访问，chmod 777 ipsearch/*
            urlretrieve(baiduapi,path)
        except Exception as e:
            country = ''
            address = ''
            time_zone = ''
            return render(request, 'ipsearch/index.html',
                          {'ipadd': ipaddress, 'country': country, 'address': address, 'time_zone': time_zone, 'error':e})
    else:
        country=''
        address=''
        time_zone=''

    return render(request,'ipsearch/index.html',{'ipadd' :ipaddress,'country':country,'address':address,'time_zone':time_zone,})

def showport(ip):
    ip=str(ip)
    ports = []
    nm=nmap.PortScanner()
    ret=nm.scan(ip,'0-10000')
    com_ports=ret['scan']
    if com_ports:
        com_ports=com_ports[ip]
        if com_ports:
            com_ports=com_ports['tcp']

            for k in com_ports.keys():
                if com_ports[k]['state']=='open':
                    ports.append(k)
            return ports
        else:
            return ports
    else:
        return ports