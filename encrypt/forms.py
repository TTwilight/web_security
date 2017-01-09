from django import forms
from datetime import datetime
# class ContactForm(forms.Form):
#     subject=forms.CharField(max_length=100)
#     message=forms.CharField(widget=forms.Textarea)  #widget参数让你指定渲染表单使用的widget类
#     sender=forms.EmailField()
#     cc_myself=forms.BooleanField(required=False)    #默认每个类型都必须有值，选择required=false使之可以没有值

class AddForm(forms.Form):
    a = forms.CharField(widget=forms.Textarea)
    b = forms.CharField(max_length=100)




