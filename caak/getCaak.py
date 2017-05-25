#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: getCaak.py 
@time: 2017/05/25 
"""

#!usr/bin/env python3.6
#-*- coding:utf-8 -*-
"""
@author:iBoy
@file: getMontsame.py
@time: 2017/05/25
"""
import requests
from lxml import etree
from mongodb_queue import MongoQueue
import multiprocessing


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
}

spider_queue = MongoQueue('mongolia', 'caak01')

def infoCrawler():
    while True:
        try:
            url = spider_queue.pop()
            print(url)
        except KeyError:
            print('队列咩有数据')
            break
        else:
            getData(url)
            spider_queue.complete(url)

def getData(url):
    respone =requests.get(url, headers=headers)
    #
    # print(respone.encoding)
    # print(respone.text)

    selector = etree.HTML(respone.text)
    all_titles = selector.xpath('//h2[@class="title"]/a')
    all_href = selector.xpath('//h2[@class="title"]/a/@href')

    for i in range(len(all_titles)):
        title = all_titles[i].xpath('string(.)')
        title = ' '.join(title.split())
        href = all_href[i]
        href = 'http://www.caak.mn' + href
        print(title + ', ' + href)
        with open('caak_urls.txt', 'a') as f:
            f.write(href + '\n')

def process_crawler():
    process= []
    # num_cpus = multiprocessing.cpu_count()
    # print('将启动进程数为: ', num_cpus)
    for i in range(50):
        p = multiprocessing.Process(target=infoCrawler)
        p.start()
        process.append(p)
    for p in process:
        p.join()

if __name__ == '__main__':
    process_crawler()
    # getData('http://www.caak.mn/?page=1600')

