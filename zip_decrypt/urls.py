from django.conf.urls import url
from . import views

name='zip_decrypt'

urlpatterns =[
    url(r'^$',views.index,name='index'),
]
