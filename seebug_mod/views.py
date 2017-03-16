from django.shortcuts import render,HttpResponse,render_to_response
import MySQLdb,pymysql
import requests
from bs4 import BeautifulSoup
import re
from .models import seebug
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
def index(request):
    # get_info('ww')
    search_content=request.POST.get('search_content')
    search_type=request.POST.get('search_type')

    if search_content:
        search_content = str(search_content)
        search_type = int(search_type)
        poc_list=search(search_content,search_type)
        paginator = Paginator(poc_list, 10)

    else:
        poc_list=seebug.objects.all().order_by('-Push_time')
        paginator=Paginator(poc_list,10)

    tiaozhuan=request.POST.get('page')
    if tiaozhuan:
        page=int(tiaozhuan)
    else:
        page=request.GET.get('page')

    pocs, before_pages, after_pages=show_page(page,paginator)  #传入当前页数,需要分页的对象

    return render(request,'seebug_mod/index.html',{'pocs':pocs,'before_pages':before_pages,'after_pages':after_pages,'search_content':search_type})
    # return render_to_response('seebug_mod/index.html', locals())
def search(content,type=1):
    if type==2:
        poc_list = seebug.objects.filter(SSV_ID__icontains=content)
        return poc_list
    elif type==3:
        poc_list = seebug.objects.filter(Push_time__icontains=content)
        return poc_list
    elif type==4:
        poc_list = seebug.objects.filter(Level__icontains=content)
        return poc_list
    else:
        poc_list = seebug.objects.filter(Poc_name__icontains=content)
        return poc_list
def show_page(page,paginator):
    try:
        pocs = paginator.page(page)
    except PageNotAnInteger:
        pocs = paginator.page(1)
    except EmptyPage:
        pocs = paginator.page(1)
    if pocs.number <= 5:
        before_pages = range(1, pocs.number)
    else:
        before_pages = range(pocs.number - 4, pocs.number)
    if pocs.number >= paginator.num_pages - 4:
        after_pages = range(pocs.number + 1, paginator.num_pages + 1)
    else:
        after_pages = range(pocs.number + 1, pocs.number + 5)

    return pocs,before_pages,after_pages

def get_info(url):
    seebug = pymysql.Connect(db='web_security', user='root', passwd='lpl2016val',charset="utf8")
    cur = seebug.cursor()
    headers={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
    }
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, 'lxml')
    vul_list=soup.find('table',attrs={'class':'table sebug-table table-vul-list'}).find('tbody').find_all('tr')
    for vul in vul_list:
        SSV_ID=re.findall('\<td\>\<a\x20href\=\"\/vuldb\/ssvid\-\d+\"\>(SSV\-\d+)\<\/a\>',str(vul))

        Push_time=re.findall('\<td\x20class\=\"text\-center\x20datetime\x20hidden\-sm\x20hidden\-xs\"\>([\d\-]+)\<\/td\>',str(vul))
        Level=vul.find('div',attrs={'data-toggle':'tooltip'})['data-original-title'].encode('utf-8')
        Poc_name=vul.find('a',attrs={'class':'vul-title'})['title'].encode('utf-8')
        Detail_link=vul.find('a',attrs={'class':'vul-title'})['href'].encode('utf-8')
        try:
            cur.execute(
                'insert into seebug_mod_seebug (SSV_ID,Push_Time,Level,Poc_name,Detail_link) VALUES (%s,%s,%s,%s,%s) ;',
                (SSV_ID, Push_time, Level, Poc_name, Detail_link))
        except:
           continue
    seebug.commit()
    cur.close()
    seebug.close()

urls=['https://www.seebug.org/vuldb/vulnerabilities?page={}'.format(str(i)) for i in range(0,200)]

for url in urls:
    get_info(url)
