from django.test import TestCase

import MySQLdb,pymysql
import requests
from bs4 import BeautifulSoup
import re
import time
from threading import Thread
# Create your tests here.
def get_info(url):
    i=1
    seebug = pymysql.Connect(db='web_security', user='root', passwd='lpl2016val',charset="utf8")
    cur = seebug.cursor()
    headers={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
    }
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, 'lxml')
    vul_list=soup.find('table',attrs={'class':'table sebug-table table-vul-list'}).find('tbody').find_all('tr')
    for vul in vul_list:
        i=i+1

        SSV_ID=re.findall('\<td\>\<a\x20href\=\"\/vuldb\/ssvid\-\d+\"\>(SSV\-\d+)\<\/a\>',str(vul))

        Push_time=re.findall('\<td\x20class\=\"text\-center\x20datetime\x20hidden\-sm\x20hidden\-xs\"\>([\d\-]+)\<\/td\>',str(vul))
        Level=vul.find('div',attrs={'data-toggle':'tooltip'})['data-original-title'].encode('utf-8')
        Poc_name=vul.find('a',attrs={'class':'vul-title'})['title'].encode('utf-8')
        Detail_link=vul.find('a',attrs={'class':'vul-title'})['href'].encode('utf-8')
        Has_cve=vul.find_all('i')[0]['data-original-title'].replace('无 CVE','无').encode('utf-8')
        Has_poc=vul.find_all('i')[1]['data-original-title'].encode('utf-8')
        Has_target=vul.find_all('i')[2]['data-original-title'].encode('utf-8')
        Has_detail=vul.find_all('i')[3]['data-original-title'].encode('utf-8')
        Has_chart=vul.find_all('i')[4]['data-original-title'].encode('utf-8')
        # Has_cve=re.findall('\<i\x20class\=\"fa\x20fa\-id\-card\x20text\-muted\x20\"\x20data\-original\-title\=\"(.*?)\"',str(vul))
        # Has_poc=re.findall('\<i\x20class\=\"fa\x20fa\-rocket\x20text\-muted\x20\"\x20data\-original\-title\=\"(.*?)\"',str(vul))
        # Has_target=re.findall('\<i\x20class\=\"fa\x20fa\-bullseye\x20text\-muted\x20\"\x20data\-original\-title\=\"(.*?)\"',str(vul))
        # Has_detail=re.findall('\<i\x20class\=\"fa\x20fa\-file\-text\-o\x20\"\x20data\-original\-title\=\"(.*?)\"',str(vul))
        # Has_chart=re.findall('\<i\x20class\=\"fa\x20fa\-signal\x20text\-muted\"\x20data\-original\-title\=\"(.*?)\"',str(vul))
        print(SSV_ID, Push_time, Level, Poc_name, Detail_link,Has_cve,Has_poc,Has_target,Has_detail,Has_chart)
        try:
            cur.execute(
                'insert into seebug_mod_seebug (SSV_ID,Push_Time,Level,Poc_name,Detail_link,Has_cve,Has_poc,Has_target,Has_detail,Has_chart) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ;',
                (SSV_ID, Push_time, Level, Poc_name, Detail_link,Has_cve,Has_poc,Has_target,Has_detail,Has_chart))
        except Exception as e :
            print(e)
            continue
    seebug.commit()
    cur.close()
    seebug.close()
    return i

urls=['https://www.seebug.org/vuldb/vulnerabilities?page={}'.format(str(i)) for i in range(0,401)]
i=1
for url in urls:
    a=get_info(url)
    i=i+a
    print(i)
print(i)