from django.shortcuts import render
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from  django.template import RequestContext
from account.models import user
# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField(label='用户名：',max_length=50)
    password = forms.CharField(label='密码：',widget=forms.PasswordInput())
    # email = forms.EmailField(label='电子邮件：')

def register(request):
    if request.method == 'POST':
        userform=UserForm(request.POST)
        if userform.is_valid():
            username=userform.cleaned_data['username']
            password=userform.cleaned_data['password']
            # email=userform.cleaned_data['email']
            User=user()
            User.username = username
            User.password = password
            # User.email=email
            User.save()
            return render(request,'account/success.html',{'username':username})


    userform=UserForm()

    return render(request,'account/register.html',{'userform':userform})

def login(request):
    if request.method == 'POST':
        userform=UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            User=user.objects.filter(username__exact= username,password__exact=password)
            if User:
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/account/login/')
        else:
            return HttpResponseRedirect('/account/login/')

    userform=UserForm()
    return render(request,'account/login.html',{'userform':userform})
