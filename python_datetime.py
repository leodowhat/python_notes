# _*_ coding:utf-8 _*_
'''
	python标准库：datetime
	author：zhanglin
	2018-05-18
'''
datetime是python自带的一个处理日期和时间的标准库。
时间在计算机中存储时通常是由timestamp表示的（数字）。
我们把1970年1月1日 00:00:00 UTC+00:00时区（格林威治标准时间）的时刻称为epoch time，记为0（1970年以前的时间timestamp为负数），当前时间就是相对于epoch time的秒数，称为timestamp。
根据定义：
	timestamp = 0 = 1970-1-1 00:00:00 UTC+0:00
	对应的北京时间为：
	timestamp = 0 = 1970-1-1 08:00:00 UTC+8:00
注意到timestamp是一个浮点数，它没有时区的概念，而datetime是有时区的.
本地时间指的是当前操作系统设定的时区。如北京时区是东八区，即 UTC+8:00
	
1. 获取当前时间
from datetime import datetime 
datetime.now() #获取当前时间
datetime.now().timestamp() #获取当前时间的邮戳/标记形式。
导入的是datetiime模块中的datetime类。
当然还有其他相关类，如：
from datetime import timezone, timedelta

2. 获取指定日期和时间
from datetime import datetime
dt = datetime(2018, 5, 18, 10, 7)
print(dt)

3. datetime转换为timestamp:

from datetime import datetime
d1 = datetime(2018, 5, 18, 10, 7)
dt.timestamp() #将datetime转换为timestamp

4. timestamp转换成datetime:
使用datetime的fromtimestamp()方法：
t2 =  1429417200.0
print(datetime.fromtimestamp(t)) # 将timestamp转换为本地时间
print(datetime.utcfromtimestamp(t)) # 转换为UTC时间，即格林威治标准时间

5. str转换为datetime
很多时候，用户输入的日期和时间是字符串，要处理日期和时间，首先必须把str转换为datetime。
转换方法是通过datetime.strptime()实现，需要一个日期和时间的格式化字符串：
from datetime import datetime
cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
print(cday)
>>> 2015-06-01 18:19:59
# 字符串'%Y-%m-%d %H:%M:%S'规定了日期和时间部分的格式
# 注意转换后的datetime是没有时区信息的。

6. datetime转换为str
如果已经有了datetime对象，要把它格式化为字符串显示给用户，就需要转换为str。
转换方法是通过strftime()实现的，同样需要一个日期和时间的格式化字符串：
from datetime import datetime
now = datetime.now()
print(now.strftime('%a, %b %d %H:%M'))
>>> Mon, May 05 16:28

7. datetime加减
加减可以直接用+和-运算符，不过需要导入timedelta这个类：
>>> from datetime import datetime, timedelta
>>> now = datetime.now()
>>> now
datetime.datetime(2015, 5, 18, 16, 57, 3, 540997)
>>> now + timedelta(hours=10)
datetime.datetime(2015, 5, 19, 2, 57, 3, 540997)
>>> now - timedelta(days=1)
datetime.datetime(2015, 5, 17, 16, 57, 3, 540997)
>>> now + timedelta(days=2, hours=12)
datetime.datetime(2015, 5, 21, 4, 57, 3, 540997)

8. 本地时间转换为UTC时间
一个datetime类型有一个时区属性tzinfo，但是默认为None。
所以无法区分这个datetime到底是哪个时区，除非通过该属性强行给datetime设置一个时区：

>>> from datetime import datetime, timedelta, timezone
>>> tz_utc_8 = timezone(timedelta(hours=8)) # 创建时区UTC+8:00
>>> now = datetime.now()
>>> now
datetime.datetime(2015, 5, 18, 17, 2, 10, 871012)
>>> dt = now.replace(tzinfo=tz_utc_8) # 强制设置为UTC+8:00
>>> dt
datetime.datetime(2015, 5, 18, 17, 2, 10, 871012, tzinfo=datetime.timezone(datetime.timedelta(0, 28800)))

9. 通过astimezone实现时区的转换
# 拿到UTC时间，并强制设置时区为UTC+0:00:
>>> utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
>>> print(utc_dt)
2016-06-17 16:13:12.377316+00:00
# astimezone()将转换时区为北京时间:
>>> bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
>>> print(bj_dt)
2016-06-17 16:13:12.377316+08:00

例子：
假设你获取了用户输入的日期和时间如2015-1-21 9:01:30，以及一个时区信息如UTC+5:00，均是str，请编写一个函数将其转换为timestamp：

import re
from datetime import datetime, timezone, timedelta

def timestamp(tr_time, tr_utc):
    #首先将用户输入的时间转为datetime
    td_time = datetime.stamp(tr_time,'%Y-%m-%d %H:%M:%S')

    #然后通过正则取得时区
    td_utc=re.match(r'^UTC([+|-]\d{1,2}):00$',tr_utc).group(1)
    td=timezone(timedelta(hours=int(td_utc)))

    #将datetime类型的时间转为UTC时间

    dt=td_time.replace(tzinfo=td)
    return dt.timestamp()




















