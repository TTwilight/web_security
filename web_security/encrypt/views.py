from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import AddForm
from Crypto.Cipher import AES
from binascii import b2a_hex,a2b_hex

# Create your views here.
def index(request):

    if request.POST.get('test')=='2':
        choice = False
        if request.method == 'POST':
            form = AddForm(request.POST)
            if form.is_valid():
                a = form.cleaned_data['a']
                b = form.cleaned_data['b']
                plaintext = AESdecrypt(a, b)
                return render(request, 'encrypt/index.html',
                              {'choice': choice,'form': form, 'plaintext': plaintext,
                               'jiemi1':'要解密的','jiemi2':'你解密的','jiemi3':'明'})
        else:
            form = AddForm()
        return render(request, 'encrypt/index.html', {'choice': choice, 'form': form})

    else:
        choice = True
        if request.method == 'POST':
            form = AddForm(request.POST)
            if form.is_valid():
                a = form.cleaned_data['a']
                b = form.cleaned_data['b']
                ciphertext = AESencrypt(a, b)
                return render(request, 'encrypt/index.html',
                              {'choice': choice,'form': form, 'ciphertext': ciphertext,
                               'jiami1': '要加密的', 'jiami2': '你加密的','jiami3':'密'})
        else:
            form = AddForm()
        return render(request, 'encrypt/index.html', {'choice': choice, 'form': form})


def AESencrypt(text,key):
    while len(str(key))%16!=0:
        key=key+'0'
    while len(str(text))%16!=0:
        text=text+' '
    mode=AES.MODE_CBC
    encrytor=AES.new(key,mode,b'0000000000000000')
    ciphertext=encrytor.encrypt(text)
    ciphertext=b2a_hex(ciphertext)
    return ciphertext

def AESdecrypt(ciphertext,key):
    while len(str(key))%16!=0:
        key=key+'0'
    mode = AES.MODE_CBC
    decrytor = AES.new(key, mode, b'0000000000000000')
    ciphertext=a2b_hex(ciphertext)
    plaintext=decrytor.decrypt(ciphertext).strip()
    return plaintext