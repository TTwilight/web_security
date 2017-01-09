from django.conf.urls import url

from .  import views

name='ipsearch'

urlpatterns=[
    url(r'^$', views.index, name='index'),
]