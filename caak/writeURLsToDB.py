#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: writeURLsToDB.py
@time: 2017/05/25 
"""
from mongodb_queue import MongoQueue

spider_queue = MongoQueue('mongolia', 'caak02')
#
for i in range(1, 1600):
    url = 'http://www.caak.mn/?page=' + str(i)

    spider_queue.push(url)



# with open('urls.txt') as f:
#     data = f.readline()
#     while data:
#         spider_queue.push(data)
#         print(data)
#         data = f.readline()
