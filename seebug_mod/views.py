from django.shortcuts import render,HttpResponse,render_to_response
import MySQLdb,pymysql
import requests
from bs4 import BeautifulSoup
import re
from .models import seebug
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import JsonResponse
import time
# Create your views here.
def index(request):
    start_time=time.time()
    search_content=request.GET.get('search_content')
    search_type=request.GET.get('search_type')
    csrfmiddlewaretoken=request.GET.get('csrfmiddlewaretoken')
    if search_content:
        search_content = str(search_content).strip()
        search_type = int(search_type)
        poc_list,counts=search(search_content,search_type)  #返回poc_list,以及相应搜索结果数量
        paginator = Paginator(poc_list, 10)

    else:
        search_content = ''
        poc_list=seebug.objects.all().order_by('-Push_time')
        counts=len(poc_list)
        paginator=Paginator(poc_list,10)

    tiaozhuan=request.POST.get('page')
    if tiaozhuan:
        page=int(tiaozhuan)
    else:
        page=request.GET.get('page')

    pocs, before_pages, after_pages=show_page(page,paginator)  #传入当前页数,需要分页的对象
    end_time=time.time()
    spend_times='%.7s' % str((end_time-start_time))  #返回耗时
    return render(request,'seebug_mod/index.html',
                  {'pocs':pocs,'before_pages':before_pages,
                   'after_pages':after_pages,'search_content':search_content,
                   'search_type':search_type,'page':page,'csrfmiddlewaretoken':csrfmiddlewaretoken,'counts':counts,'spend_times':spend_times})
    # return render_to_response('seebug_mod/index.html', locals())
def search(content,type=1):
    if type==2:  #按SSV_ID查询
        poc_list = seebug.objects.filter(SSV_ID__icontains=content).order_by('-Push_time')
        return poc_list,len(poc_list)
    elif type==3: #按提交时间查询
        poc_list = seebug.objects.filter(Push_time__icontains=content).order_by('-Push_time')
        return poc_list,len(poc_list)
    elif type==4: #按漏洞等级查询
        poc_list = seebug.objects.filter(Level__icontains=content).order_by('-Push_time')
        return poc_list,len(poc_list)
    elif type==5: #按有无CVE查询
        poc_list = seebug.objects.filter(Has_cve__icontains=content).order_by('-Push_time')
        return poc_list,len(poc_list)
    elif type==6: #按有无Poc查询
        poc_list = seebug.objects.filter(Has_poc__icontains=content).order_by('-Push_time')
        return poc_list,len(poc_list)
    elif type==7: #按有无靶场查询
        poc_list = seebug.objects.filter(Has_target__icontains=content).order_by('-Push_time')
        return poc_list,len(poc_list)
    elif type==8: #按有无详情查询
        poc_list = seebug.objects.filter(Has_detail__icontains=content).order_by('-Push_time')
        return poc_list,len(poc_list)
    elif type==9: #按有无图表查询
        poc_list = seebug.objects.filter(Has_chart__icontains=content).order_by('-Push_time')
        return poc_list,len(poc_list)
    else:       #按漏洞名称查询
        poc_list = seebug.objects.filter(Poc_name__icontains=content).order_by('-Push_time')
        return poc_list,len(poc_list)
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
def ajax_chart(request):
    all=len(seebug.objects.all())
    cve_table=str((all-len(seebug.objects.filter(Has_cve__icontains='无')))/all*100)+'%'
    poc_table=str((all-len(seebug.objects.filter(Has_poc__icontains='无 PoC')))/all*100)+'%'
    target_table=str((all-len(seebug.objects.filter(Has_target__icontains='无靶场')))/all*100)+'%'
    detail_table=str((all-len(seebug.objects.filter(Has_detail__icontains='无详情')))/all*100)+'%'
    chart_table=str((all-len(seebug.objects.filter(Has_chart__icontains='无影响图表')))/all*100)+'%'
    seebug_table_dict={
        'all':all,
        'cve_table':cve_table,
        'cve_count':(all-len(seebug.objects.filter(Has_cve__icontains='无'))),
        'poc_table':poc_table,
        'poc_count':(all-len(seebug.objects.filter(Has_poc__icontains='无 PoC'))),
        'target_table':target_table,
        'target_count':(all-len(seebug.objects.filter(Has_target__icontains='无靶场'))),
        'detail_table':detail_table,
        'detail_count':(all-len(seebug.objects.filter(Has_detail__icontains='无详情'))),
        'chart_table':chart_table,
        'chart_count':(all-len(seebug.objects.filter(Has_chart__icontains='无影响图表'))),

    }
    return JsonResponse(seebug_table_dict)

# def get_info(url):
#     seebug = pymysql.Connect(db='web_security', user='root', passwd='lpl2016val',charset="utf8")
#     cur = seebug.cursor()
#     headers={
#         'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
#     }
#     html = requests.get(url, headers=headers).content
#     soup = BeautifulSoup(html, 'lxml')
#     vul_list=soup.find('table',attrs={'class':'table sebug-table table-vul-list'}).find('tbody').find_all('tr')
#     for vul in vul_list:
#         SSV_ID=re.findall('\<td\>\<a\x20href\=\"\/vuldb\/ssvid\-\d+\"\>(SSV\-\d+)\<\/a\>',str(vul))
#
#         Push_time=re.findall('\<td\x20class\=\"text\-center\x20datetime\x20hidden\-sm\x20hidden\-xs\"\>([\d\-]+)\<\/td\>',str(vul))
#         Level=vul.find('div',attrs={'data-toggle':'tooltip'})['data-original-title'].encode('utf-8')
#         Poc_name=vul.find('a',attrs={'class':'vul-title'})['title'].encode('utf-8')
#         Detail_link=vul.find('a',attrs={'class':'vul-title'})['href'].encode('utf-8')
#         Has_cve=vul.find('i',attrs={'data-toggle':'tooltip','class':'fa fa-id-card'})['data-original-title'].encode('utf-8')
#         Has_poc=vul.find('i',attrs={'data-toggle':'tooltip','class':'fa fa-rocket'})['data-original-title'].encode('utf-8')
#         Has_target=vul.find('i',attrs={'data-toggle':'tooltip','class':'fa fa-bullseye'})['data-original-title'].encode('utf-8')
#         Has_detail=vul.find('i',attrs={'data-toggle':'tooltip','class':'fa fa-file-text-o'})['data-original-title'].encode('utf-8')
#         Has_chart=vul.find('i',attrs={'data-toggle':'tooltip','class':'fa fa-signal'})['data-original-title'].encode('utf-8')
#         try:
#             cur.execute(
#                 'insert into seebug_mod_seebug (SSV_ID,Push_Time,Level,Poc_name,Detail_link,Has_cve,Has_poc,Has_target,Has_detail,Has_chart) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ;',
#                 (SSV_ID, Push_time, Level, Poc_name, Detail_link,Has_cve,Has_poc,Has_target,Has_detail,Has_chart))
#         except:
#            continue
#     seebug.commit()
#     cur.close()
#     seebug.close()
#
# urls=['https://www.seebug.org/vuldb/vulnerabilities?page={}'.format(str(i)) for i in range(0,200)]
#
# for url in urls:
#     get_info(url)
