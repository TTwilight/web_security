from django.conf.urls import url
from . import views

name='hacktools'

urlpatterns =[
    url(r'^$',views.index,name='index'),
]
