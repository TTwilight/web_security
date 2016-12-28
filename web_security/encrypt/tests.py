from django.test import TestCase
from Crypto.Cipher import AES
# Create your tests here.
def AESencrypt(key,text):
    mode=AES.MODE_CBC
    encrytor=AES.new(key,mode, b'0000000000000000')
    ciphertext=encrytor.encrypt(text)
    return ciphertext

a='22222222222222222222222222222222'
b='2222222222222222'
C=AESencrypt(a,b)
print(C)