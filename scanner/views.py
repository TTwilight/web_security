from django.shortcuts import render

# Create your views here.
from urllib.request import Request,urlopen
import nmap,socket

def index(request):
    host=request.POST.get('host_name')
    if host:
        hostname = host.strip()
        host=host.strip()
        try:
            host = socket.gethostbyname(host)
            tcps=showport(host)
            return render(request,'scanner/index.html',{'tcps':tcps,'host':hostname,})
        except Exception as e:
            tcps = ['0']

            return render(request, 'scanner/index.html', {'tcps': tcps,'error':e })
    else:
        tcps=['0']
        return render(request, 'scanner/index.html', {'tcps': tcps, })
def showport(host):
    host=str(host)
    ports = []
    nm=nmap.PortScanner()
    result=nm.scan(host,'0-10000')
    if result['scan']:
        tcps=result['scan'][host]['tcp']
        return tcps
    else:
        tcps=''
        return tcps

