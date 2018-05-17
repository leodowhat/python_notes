# _*_ coding:utf-8 _*_
'''
	协程Coroutine学习笔记——yield和yield from的使用
	author：zhanglin
	2018-05-09
'''
# 协程+生成器+yield
生成器的调用方式：next调用+循环调用+循环中调用next
1 小内存占用下读取大文件：
def read_file(fpath):
	Block_size = 1024
	with open(fpath, 'rb') as f:
		block = f.read(Block_size)
		if block:
			yield block
		else:
			return
#若直接调用文件对象的read()方法会到时不可控的内存占用。

2 生产器的特性使用：
	next()：获取下一个返回值,相当于send(None)。#即，若a为一生成器，a.send(None)与a.next()作用一样！
	send(b)：向生成器传入参数b #第一次send的参数必须是None，用于初始化生成器！！！！
	throw(ValueError):向yield抛出ValueError异常+获取下一个返回值
	close():退出生成器
#可以将生成器理解为一个特定的函数，其允许返回一个中间值，然后挂起代码的执行，稍后再恢复执行。

3 生成器表达式
#列表解析是一次性在内存中生产所有的数据，用以创建列表对象，所以不适合迭代大量的数据。
#生成器表达式是列表解析的扩展，直观的看只是把列表的中括号换成了括号，返回一个生成器对象。
列表解析：
	[expr for iter_var in iterable if cond_expr]
生成器表达式：
	(expr for iter_var in iterable if cond_expr)

例子，查找文件中最长的行：
#使用file文件内置的迭代器+列表解析
f = open('FILENAME', 'r')
allLinesLen = [line(x.strip()) for x in f]
f.close()
return max(allLinesLen)   # 返回列表中最大的数值

#使用file文件内置的迭代器+生成器
f = open('FILENAME', 'r')
allLinesLen = (line(x.strip()) for x in f)   # 这里的 x 相当于 yield x
f.close()
return max(allLinesLen)
#进一步简化：
f = open('FILENAME', 'r')
longest = max(line(x.strip()) for x in f)
f.close()
return longest

4. 生成器的唯一注意事项就是：生成器只能遍历一次。

def get_province_population(filename):
    with open(filename) as f:
        for line in f:
            yield int(line)

gen = get_province_population('data.txt')
all_population = sum(gen)
#print all_population
for population in gen:
    print population / all_population
#执行上述代码将不会输出任何记过。这是因为，生成器只能遍历一次。
#在我们执行sum语句的时候，就遍历了我们的生成器，当我们再次遍历我们的生成器的时候，将不会有任何记录。所以，上面的代码不会有任何输出。

5. yield from 的使用
简单讲，yield from a 就相当于: 
	for i in a:
		yield i
例子：
def myfun1(total):
    for i in range(total):
        yield i
    yield from ['a', 'b', 'c']
def myfun2(total):
    for i in range(total):
        yield i
    for i in ['a', 'b', 'c']:
        yield i
#函数myfun1就相当于函数myfun2	。
>>> m = myfun1(3)
>>> next(m)
0
>>> next(m)
1
>>> next(m)
2
>>> next(m)
'a'
>>> next(m)
'b'
>>> next(m)
'c'
>>> next(m)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration	

6. yield 空
此时，“yield空”相当与一个中断器，循环运行到这里会中断，用于辅助其他程序的执行。也可以理解成返回值是None。
def myfun(total):
	for i in range(total):
		print(i+1)
		yield

a = myfun(4)		
>>> next(a)
1
>>> next(a)
2
>>> next(a)
3		
	
7. return yield的用法
其中return只是起到终止函数的作用。
例：下面两种实现，效果相同
def myfun1(total):
	yield from range(total)
	
def myfun2(total):
	return(yield from range(total))
	
a1 = myfun1(4)
a2 = myfun2(4)
#print(i for i in a1)与print(i for i in a2)输出相同。

例：下面两种就不同了（return 后的语句就不会执行了）
def myfun1(total):
	yield from range(total)
	yield 1
	
def myfun2(total):
	return(yield from range(total))
	yield 1#此语句不会被执行

使用协程实现一个生产消费者的例子：
'''
协程最大的优势就是协程极高的执行效率。因为子程序切换不是线程切换，而是由程序自身控制，
因此，没有线程切换的开销，和多线程比，线程数量越多，协程的性能优势就越明显。
第二大优势就是不需要多线程的锁机制，因为只有一个线程，也不存在同时写变量冲突，
在协程中控制共享资源不加锁，只需要判断状态就好了，所以执行效率比多线程高很多。
因为协程是一个线程执行，那怎么利用多核CPU呢？最简单的方法是多进程+协程，
既充分利用多核，又充分发挥协程的高效率，可获得极高的性能.
'''
#下面是廖雪峰老师教程的例子：
def consumer():
	r = ''
	while True:
		n = yield r
		if n is not None:
			print('[CONSUMER] Consuming %s...' % n)
			r = '200 OK'
			
def produce(c):
	c.send(None)
	n = 0
	while n < 5:
		n = n+1
		print('[PRODUCER] Producing %s...' % n)
		r = c.send(n)
		print('[PRODUCER] Consumer return %s' % r)
	c.close()
	
c = consumer()
produce(c)

'''
[PRODUCER] Producing 1...
[CONSUMER] Consuming 1...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 2...
[CONSUMER] Consuming 2...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 3...
[CONSUMER] Consuming 3...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 4...
[CONSUMER] Consuming 4...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 5...
[CONSUMER] Consuming 5...
[PRODUCER] Consumer return: 200 OK
'''
下面的代码可以不使用看似高大上的协程实现上述生产者消费者模型的功能：
def consumer(n):
	if not n:
		return
	print('[CONSUMER] Consuming %s...' % n)
	return '200 OK'

def produce():
	n = 0
	while n < 5:
		n = n + 1
		print('[PRODUCER] Producing %s...' % n)
		r = comsumer(n)
		print('[PRODUCER] Consumer return %s' % r)
		
produce()


