from django.conf.urls import url
from . import views

app_name='account'

urlpatterns=[
    url(r'^$', views.login, name='login1'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
]