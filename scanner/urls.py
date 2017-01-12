from django.conf.urls import url
from . import views

name = 'scanner'

urlpatterns=[
    url('^$',views.index,name='index'),
]