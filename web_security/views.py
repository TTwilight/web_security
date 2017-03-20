from django.shortcuts import render
from django.http import HttpResponse,Http404
from urllib.request import urlopen,urlretrieve
from bs4 import BeautifulSoup
import json
import os
from binascii import a2b_hex,b2a_hex

import json
def home(request):

    return render(request,'home.html')