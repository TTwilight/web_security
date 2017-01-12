from django.test import TestCase

# Create your tests here.
import nmap

s=input()
s=str(s)
nm=nmap.PortScanner()
result=nm.scan(s)
print(result)