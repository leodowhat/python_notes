# _*_ coding:utf-8 _*_
'''
	gevent模块和grequests模块的使用
	author：zhanglin
	2018-05-10
'''
#gevent是一个异步模块
#gevent本质上是开启了多个微线程！！！！！！！
import gevent
from gevent import monkey
import requests
from bs4 import BeautifulSoup
import threading

monkey.patch_all() # 相当于对IO操作打上补丁， 固定加上该语句
# monkey.patch_all(thread=False)  # 该语句即为不使用多个微线程仅仅用一个线程来完成任务
def get_title(i):
	print(threading.current_thread().name) # 打印出当前线程名称
	url = 'https://movie.douban.com/top250?start={}&filter='.format(i*25)
	text = requests.get(url).content
	soup = BeautifulSoup(text, 'html.parser')
	lis = soup.find('ol', class_='grid_view').find_all('li')
	for li in lis:
		title = li.find('span', class_='title').text
		print(title)

gevent.joinall([gevent.spawn(get_title, i) for i in range(10)])
'''
运行结果首先打印出了下面内容
DummyThread-1 # 微线程
DummyThread-2
DummyThread-3
DummyThread-4
DummyThread-5
DummyThread-6
DummyThread-7
DummyThread-8
DummyThread-9
DummyThread-10
'''

# requests库的作者将requests和gevent融合产生了grequests模块，专门用于异步网络请求。

import grequests
from bs4 import BeautifulSoup

def get_title(rep):
    soup = BeautifulSoup(rep.text, 'html.parser')
    lis = soup.find('ol', class_='grid_view').find_all('li')
    for li in lis:
        title = li.find('span', class_="title").text
        print(title)

reps = (grequests.get('https://movie.douban.com/top250?start={}&filter='.format(i*25)) for i in range(10))
for rep in grequests.map(reps):
    get_title(rep)
	
	
