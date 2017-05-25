#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: getContent.py 
@time: 2017/05/25 
"""

import requests
from lxml import etree
from mongodb_queue import MongoQueue
import multiprocessing

url = 'http://www.sonin.mn/news/politics-economy/26088'
# url = 'http://www.sonin.mn/news/politics-economy/26006'
url = 'http://www.sonin.mn/news/politics-economy/26088'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0'
}


spider_queue = MongoQueue('mongolia', 'sonin_urls')


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
    try:
        response = requests.get(url, headers=headers)
        # print(response.text)
        #
        # with open('html', 'r') as f:
        #     response_text = f.readlines()

        selector = etree.HTML(response.text)

        title = selector.xpath('//h1')[0].xpath('string(.)')
        # print(title)


        time = selector.xpath('//p[@class="news-other-text"]')[0].xpath('string(.)')
        print(time)


        # all_text = selector.xpath('//div[@id="text-show"]//br/following-sibling::text()')
        all_text = selector.xpath('//div[@id="text-show"]//p')
        if len(all_text) == 0: #判断方法待检验
            all_text = selector.xpath('//div[@id="text-show"]/div[@style="text-align: justify;"]')
        sumContent = ''
        for i in range(len(all_text)):
            text = all_text[i].xpath('string(.)')
            text = '<p>' + text + '</p>'
            text = text.replace('\^M', '')
            text = ' '.join(text.split())
            text =text.replace('\\t', '')
            text = text.replace('\', \'', '')

            sumContent = sumContent + text
            print(text)


        all_reviews = selector.xpath('//p[@class="comment-show"]') # 挽救第一句 br不处理 直接p
        if len(all_reviews) == 0:
            all_reviews = selector.xpath('//div[@class="socialtabinformation"]//p')
        sumReview = ''
        for i in range(len(all_reviews)):
            review = all_reviews[i].xpath('string(.)')
            review = '<p>' + review + '</p>'
            #多余空格处理等
            review = ' '.join(review.split())
            sumReview = sumReview + review

        result = '{' + '"title": ' + '"' + title + '", ' + '"url": ' + '"' + url + '", ' + '"review": ' + '"' + sumReview + '", ' + '"content": ' + '"' + sumContent + '", ' + '"time": ' + '"' + time + '", ' + '"type": ' + '"news"' + '}'
        print(result)

        if len(title) > 1:  # there exist data
            with open('soninData.txt', 'a') as file:
                file.write(result + '\n')
    except Exception as e:
        print(e)


def process_crawler():
    process= []
    # num_cpus = multiprocessing.cpu_count()
    # print('将启动进程数为: ', num_cpus)
    for i in range(10):
        p = multiprocessing.Process(target=infoCrawler)
        p.start()
        process.append(p)
    for p in process:
        p.join()

if __name__ == '__main__':
    process_crawler()
    # getData(url)