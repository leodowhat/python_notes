# _*_ coding:utf-8 _*_
'''
	异步asyncio学习笔记
	author：zhanglin
	2018-05-07
'''
常见使用方式1：
import asyncio

async def myfun(i):
	print('start {}th'.format(i))
	await asyncio.sleep(1)
	print('start {}th'.format(i))
	
loop = asyncio.get_event_loop()
myfun_list = (myfun(i) for i in range(10))
loop.run_until_complete(asyncio.gather(*myfun_list))

常见使用方式2：

import asyncio

async def myfun(i):
	print('start {}th'.format(i))
	await asyncio.sleep(1)
	print('start {}th'.format(i))
	
loop = asyncio.get_event_loop()
myfun_list = [asyncio.ensure_future(myfun(i)) for i in range(10)]
loop.run_until_complete(asyncio.wait(myfun_list))
#两种常用方式其实就最后两行不同，即使用的是gather还是wait

与之前学过的多线程、多进程相比，asyncio模块有一个非常大的不同：传入的函数不是随心所欲。
若将myfun函数中的await asyncio.sleep(1)换成time.sleep(1)，程序则不再是异步的，而是同步执行，运行十秒。
所以，将myfun函数换成爬虫抓取页面的函数(代码如下所示)，仍然不会异步执行：
import asyncio
import requests
from bs4 import BeautifulSoup

async def get_title(a):
    url = 'https://movie.douban.com/top250?start={}&filter='.format(a*25)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    lis = soup.find('ol', class_='grid_view').find_all('li')
    for li in lis:
        title = li.find('span', class_="title").text
        print(title)

loop = asyncio.get_event_loop()
fum_list = (get_title(i) for i in range(10))
loop.run_until_complete(asyncio.gather(*fun_list))


对于上述get_title()函数，asyncio库只能通过添加线程的方式实现异步。
下面代码中通过run_in_executor()开启新的线程，并协调各个线程，实现了time.sleep时的异步：

import asyncio
import time

def myfun(i):
    print('start {}th'.format(i))
    time.sleep(1)
    print('finish {}th'.format(i))
	
async def main():
	loop = asyncio.get_event_loop()
	futures = (loop.run_in_excutor(None, myfun, i) for i in range(10))
	for result in await asyncio.gather(*futures):
		pass

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
		
要想实现完全异步，即上述程序10次循环的结果一次性打印出来，则开启的线程必须足够多，10次循环则需要10个线程：

import concurrent.future as cf
import asyncio
import time

def myfun(i):
    print('start {}th'.format(i))
    time.sleep(1)
    print('finish {}th'.format(i))

async def main():
	with cf.ThreadPoolExecutor(max_worker = 10) as executor:#此时开启了10个线程
		loop = asyncio.get_event_loop()
		futures = (loop.run_in_excutor(excutor, myfun, i) for i in range(10))
		#对比67行中的run_in_excutor()传入的参数，None变成了excutor，从而设定了执行任务的线程个数——10个。
		for result in await asyncio.gather(*futures):
			pass
			
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
		
同样的方式，即通过开启多个线程实现了异步爬虫：
import concurrent.futures as cf
import asyncio
import requests
from bs4 import BeautifulSoup

def get_title(i):
    url = 'https://movie.douban.com/top250?start={}&filter='.format(i*25)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    lis = soup.find('ol', class_='grid_view').find_all('li')
    for li in lis:
        title = li.find('span', class_="title").text
        print(title)

async def main():
    with cf.ThreadPoolExecutor(max_workers = 10) as executor:
        loop = asyncio.get_event_loop()
        futures = (
            loop.run_in_executor(
                executor,
                get_title, 
                i)
            for i in range(10)
            )
        for result in await asyncio.gather(*futures):
            pass

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

要想实现只开一个线程下的异步爬虫，就需要使用await()，而使用await,必须是一个awaitable对象，这是不能使用requests的原因。
下面使用aiohttp模块实现：

import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def get_title(i):
    url = 'https://movie.douban.com/top250?start={}&filter='.format(i*25)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(resp.status)
            text = await resp.text()
            print('start', i)
    soup = BeautifulSoup(text, 'html.parser')
    lis = soup.find('ol', class_='grid_view').find_all('li')
    for li in lis:
        title = li.find('span', class_="title").text
        print(title)

loop = asyncio.get_event_loop()
fun_list = (get_title(i) for i in range(10))
loop.run_until_complete(asyncio.gather(*fun_list))	
		
		
		
		
		
		
		
		
		
		
		
		