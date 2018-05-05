# _*_ coding:utf-8 _*_
'''
	python多进程练习
	author：zhanglin
	2018-05-05
'''
#多进程与多线程最大的不同在于，多进程的每一个进程都有一份变量的拷贝，进程之间的操作互不影响.
#创建进程的代码一定要放在if __name__ == '__main__'里面。
#进程间交流的方式有多种：队列、管道pipe等。

import multiprocessing
import time

def myfun(num):
    time.sleep(1)
    print(num + 1)

if __name__ == '__main__':
    for i in range(5):
        p = multiprocessing.Process(target = myfun, args = (i, ))
        p.start()
#以上是最简单的进程代码展示。。

类的形式：
import multiprocessing
import requests
from bs4 import BeautifulSoup

class MyProcess(multiprocessing.Process):

    def __init__(self, i):
        multiprocessing.Process.__init__(self)
        self.i = i

    def run(self):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(self.i*25)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        lis = soup.find('ol', class_='grid_view').find_all('li')
        for li in lis:
            title = li.find('span', class_="title").text
            print(title)

if __name__ == '__main__':
    for i in range(10):
        p = MyProcess(i)
        p.start()
		
进程池：
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool, current_process

def get_title(i):
    print('start', current_process().name)
    title_list = []
    url = 'https://movie.douban.com/top250?start={}&filter='.format(i*25)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    lis = soup.find('ol', class_='grid_view').find_all('li')
    for li in lis:
        title = li.find('span', class_="title").text
        # return title
        title_list.append(title)
        print(title)
    return(title_list)

if __name__ == '__main__':
    pool = Pool()
    for i in range(10):
        pool.apply_async(get_title, (i, ))
    pool.close()
    pool.join()
    print('finish')
#Pool默认为CPU核心数量（逻辑处理器的数量，不是内核数）。进程数理论上可以非常大，成百上千都行，但数量开启太多会造成切换费时，反而效率降低。
	
进程间通信——队列：
#multiprocessing模块中提供了multiprocessing.Queue，它和Queue.Queue的区别在于，它里面封装了进程之间的数据交流，不同进程可以操作同一个multiprocessing.Queue。
from multiprocessing import Process, Queue

def addone(q):
    q.put(1)

def addtwo(q):
    q.put(2)

if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=addone, args = (q, ))
    p2 = Process(target=addtwo, args = (q, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(q.get())
    print(q.get())
#该队列是线程、进程安全的，即对队列的每一次修改中间不会被中断从而造成结果错误。

进程间通信——pipe:
#pipe的功能与Queue类似，可以理解为简化版的Queue.
import random
import time
from multiprocessing import Process, Pipe, current_process
def produce(conn):
    while True:
        new = random.randint(0, 100)
        print('{} produce {}'.format(current_process().name, new))
        conn.send(new)
        time.sleep(random.random())
def consume(conn):
    while True:
        print('{} consume {}'.format(current_process().name, conn.recv()))
        time.sleep(random.random())
if __name__ == '__main__':
    pipe = Pipe()
    p1 = Process(target=produce, args=(pipe[0],))
    p2 = Process(target=consume, args=(pipe[1],))
    p1.start()
    p2.start()
#上面使用了pipe来实现生产消费模式	
总结Queue与pipe之间的差别如下:
1. Queue使用put get来维护队列，pipe使用send recv来维护队列
2. pipe只提供两个端点，而Queue没有限制。这就表示使用pipe时只能同时开启两个进程，可以像上面一样，一个生产者一个消费者，
   它们分别对这两个端点（Pipe()返回的两个值）操作，两个端点共同维护一个队列。如果多个进程对pipe的同一个端点同时操作，
   就会发生错误（因为没有上锁，类似线程不安全）。所以两个端点就相当于只提供两个进程安全的操作位置，以此限制了进程数量只能是2
3. Queue的封装更好，Queue只提供一个结果，它可以被很多进程同时调用；而Pipe()返回两个结果，要分别被两个进程调用
4. Queue的实现基于pipe，所以pipe的运行速度比Queue快很多
5. 当只需要两个进程时使用pipe更快，当需要多个进程同时操作队列时，使用Queue!!!
	
进程间通信——value:
#除了Value,python的多进程模块还提供了类似的Array。
from multiprocessing import Process, Value
def f1(n):
    n.value += 1
def f2(n):
    n.value -= 2
if __name__ == '__main__':
    num = Value('d', 0.0)#d表示双精度浮点数
    p1 = Process(target=f1, args=(num, ))
    p2 = Process(target=f2, args=(num, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(num.value)	

进程锁：
#变量在进程间共享后容易出现问题，故需要用进程锁来保证安全！
lock = multiprocessing.Lock()
lock.acquire()
lock.release()
with lock:	
这些用法和功能都和多线程是一样的
另外，multiprocessing.Semaphore Condition Event RLock也和多线程相同	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	