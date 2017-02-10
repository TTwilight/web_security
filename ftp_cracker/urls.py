from django.conf.urls import url
from . import views

name = 'ftp_cracker'

urlpatterns = [
    url(r'^$',views.index,name='index'),
]