# _*_ coding:utf-8 _*_
'''
	selenium爬取动态网页(腾讯动漫：http://ac.qq.com)
	author：zhanglin
	2018-05-19
'''
import requests
import json
import selenium.webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import os
import random

os.environ["LANG"] = "en_US.UTF-8"

def scroll(n,i):
    return "window.scrollTo(0,(document.body.scrollHeight/{0})*{1}*80);".\
        format(n,i)
		
def crawl_pictures(url):
    comics={}
    comic_url=[]
    #driver = selenium.webdriver.Chrome()
    driver = selenium.webdriver.PhantomJS()
    #driver.implicitly_wait(30)
    driver.set_page_load_timeout(30)
    #url='http://ac.qq.com/ComicView/index/id/543606/cid/1'
    #url='https://manhua.163.com/reader/4639712296520118385/4643138479170091194#scale=7@imgIndex=8'
    driver.get(url)
    time.sleep(4)
    n = 20
    for i in range(0,n+1):
        s = scroll(n,i)
        print(s)
        driver.execute_script(s)
        time.sleep(random.randint(1, 10))


    content=driver.page_source

    #print (content)
    soup = BeautifulSoup(content,"lxml")
    if '163' in url:
        comic_list=soup.find_all('img',attrs = {'draggable' : 'false'})
        for i in comic_list:
            print(i)
            try:
                image_src=i['src']
            except Exception as e:
                print (e)
            print (image_src)

    else:

        comic_list=soup.find_all('li',attrs = {'style' : True})
        comic_title=soup.find('span',attrs = {'class' : 'title-comicHeading'}).text.strip()
        comic_title=comic_title.replace('/',' ')
        for i in comic_list:
            #image_num=0
            try:
                #image_num=i.find('em').text.strip()
                image_url=i.find('img')['src']
                #print(image_url)
                comic_url.append(image_url)
            except Exception as e:
                print (e)

        comics['title']=comic_title
        comics['url']=comic_url
            #print (image_num)
            #print (image_url)

            #break
    return comics
    #print (content)
    #soup = BeautifulSoup(content,"lxml")	
	
def download(comics):
    #directory='d:\\manhua\\'+directory
    title=comics['title']
    urls=comics['url']
    directory='d:\\manhua\\幽游白书\\'+title
	
	if not os.path.exists(directory):
		os.mkdir(directory)
 
    for download_link in urls:
        time.sleep(random.randint(1, 10))
        fname=directory+'\\'+str(urls.index(download_link)+1)+'.png'
        if os.path.exists(fname):
            #pass
            print ('File '+fname+' is already exists,SKIP......')
        else:
        #     print ('Folder is already exists,Downloding '+directory+'.....Please Waiting')
            r=requests.get(download_link)
            with open (fname,"wb") as code:
                code.write(r.content)
            print(fname+' Download Compelte')


	
if __name__ = "__mian__":
	url = 
	
	for i in range(1, 3): # 更改需要爬取多少话
		url_chapter = 'http://ac.qq.com/ComicView/index/id/543606/cid/2' + str(i)
		print('Now Crawling Chapter' + str(i) + '...almost need waiting 30 seconds.')
		time.sleep(random.randint(20, 40))
		content = crawl_pictures(url_chapter)
		download(content)
		print('Crawling of Chapter' + str(i) + 'is completed !')
		
		



