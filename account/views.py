from django.shortcuts import render
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from  django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import hashers,authenticate,login,logout
# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=50)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件')

class UserForm2(forms.Form):
    username = forms.CharField(label='用户名',max_length=50)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())

def register(request):
    if request.method == 'POST':
        userform=UserForm(request.POST)
        if userform.is_valid():
            username=userform.cleaned_data['username']
            password=userform.cleaned_data['password']
            email=userform.cleaned_data['email']
            if len(password)<8:
                error = '密码不能少于8位！'
                return render(request, 'account/register.html', {'error': error})
            else:
                try:
                    user=User.objects.create_user(username,email,password)
                    user.save()
                except Exception :
                    error='该用户名已存在！'
                    return render(request, 'account/register.html', {'error': error})
                return render(request,'account/success.html',{'new':True,'username':username})


    userform=UserForm()

    return render(request,'account/register.html',{'userform':userform})

def login_ok(request):
    if request.method == 'POST':
        userform=UserForm2(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            user=authenticate(username=username,password=password)

            if user.is_active:
                login(request,user)
                return render(request, 'account/success.html', {'username': username})
            else:
                return HttpResponseRedirect('/seebug_mod/')
        else:
            return HttpResponseRedirect('/account/login/')

    userform=UserForm2()
    return render(request,'account/login.html',{'userform':userform})


def loginout(request):
    logout(request)
    return HttpResponseRedirect('/account/login/')
