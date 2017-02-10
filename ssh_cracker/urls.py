from django.conf.urls import url
from . import views

name='ssh_cracker'

urlpatterns = [
    url(r'^$',views.index,name='index'),
]