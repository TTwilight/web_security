from django.conf.urls import url
from . import views

app_name='account'

urlpatterns=[
    url(r'^$', views.login_ok, name='login1'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_ok, name='login'),
    url(r'^loginout/$', views.loginout, name='loginout'),
]