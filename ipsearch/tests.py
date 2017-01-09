import nmap
from nmap import nmap

nm=nmap.PortScanner()
ret=nm.scan('63.216.57.147','20-5000')
a=nm.command_line()
print(ret['scan']['63.216.57.147']['tcp'])
print(a)
# print(nmap.__file__)
