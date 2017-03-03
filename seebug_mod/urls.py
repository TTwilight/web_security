from django.conf.urls import url
from . import views
name='seebug_mod'

urlpatterns=[
    url(r'^$',views.index,name='index'),
]