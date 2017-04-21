from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import AddForm
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from binascii import b2a_hex,a2b_hex
import base64
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    a= request.POST
    if len(a)==0:
        form=AddForm()
        return render(request, 'encrypt/index.html', {'form': form})
    else:
        form=AddForm(request.POST)

        if form.is_valid():
            a=form.cleaned_data['a']
            b=form.cleaned_data['b']

            type=request.POST.get('jiami_type')
            action=request.POST.get('jiami_action')
            if type=='a':
                if action=='1':
                    text=AESencrypt(a,b)
                    zhuangtai = '当前状态为AES加密:'
                elif action=='2':
                    text=AESdecrypt(a,b)
                    zhuangtai = '当前状态为AES解密:'
                else:
                    text = '错误：请选择加密操作'
                    zhuangtai = '错误：请选择加密操作'
            elif type=='b':
                if action=='1':
                    text=text=DESencrypt(a,b)
                    zhuangtai = '当前状态为DES加密:'
                elif action=='2':
                    text = '错误：请选择加密操作'
                    zhuangtai = '错误：请选择加密操作'
                else:
                    text='error2'
                    zhuangtai = '错误：'
            else:
                text='错误：请选择加密算法'
                zhuangtai='错误：请选择加密操作'
            return render(request, 'encrypt/index.html', {'form': form,'text':text,'zhuangtai':zhuangtai})
        else:
            return HttpResponse("出错了")

def AESencrypt(text,key):
    while len(str(key))%16!=0:
        key=key+'0'
    while len(str(text))%16!=0:
        text=text+' '
    mode=AES.MODE_CBC
    encryptor=AES.new(key,mode,b'0000000000000000')
    ciphertext=encryptor.encrypt(text)
    ciphertext=b2a_hex(ciphertext)
    ciphertext=base64.b64encode(ciphertext)
    return ciphertext

def AESdecrypt(ciphertext,key):
    while len(str(key))%16!=0:
        key=key+'0'
    mode = AES.MODE_CBC
    decrytor = AES.new(key, mode, b'0000000000000000')
    plaintext=base64.b64decode(ciphertext)
    plaintext=a2b_hex(plaintext)
    plaintext=decrytor.decrypt(plaintext).strip()
    return plaintext

def DESencrypt(text,key):
    while len(str(key)) % 8 != 0:
        key = key + '0'
    while len(str(text)) % 8 != 0:
        text = text + ' '
    mode=DES.MODE_CBC
    encryptor=DES.new(key,mode,b'00000000')
    ciphertext=encryptor.encrypt(text)
    ciphertext=b2a_hex(ciphertext)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext

def DESdecrypt(ciphertext,key):
    while len(str(key))%8!=0:
        key=key+'0'
    mode = DES.MODE_CBC
    decrytor = DES.new(key, mode, b'00000000')
    plaintext=base64.b64decode(ciphertext)
    plaintext=a2b_hex(plaintext)
    plaintext=decrytor.decrypt(plaintext).strip()
    return plaintext
    