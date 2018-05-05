# _*_ coding:utf-8 _*_
'''
	sqlalchemy官方文档学习笔记
	author：zhanglin
	2018-05-04
'''
# 版本查询（命令行模式）
import sqlalchemy
sqlalchemy.__version__

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)
#echo是一个flag，由python的logging模块实现，用于输出执行的SQL语句。
#create_engine函数返回一个Engine的实例，它通过dialect处理与数据库及所用DBAPI的所有细节，是与数据库交互的核心接口。
#当调用Engine.execute()或Engine.connect()方法时，Engine实例就会创建一个真实的与数据库的DBAPI连接。

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
#通过Declarative system定义classes mapped。需要先通过declarative_base()函数得到基类base class。

from sqlalchemy import Column, Integer, String

class User(Base):
	__tablename__ = 'users'
	#该属性是必不可少的。
	
	id = Column(Integer, primary_key = True)
	#设为主键，并且为整数Integer的属性会自动被设置为自增的，即autoincrement=True
	name = Column(String)
	fullname = Column(String)
	password = Column(String)
	
	def __repr__(self):
		return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)
	#该方法是可选的，用于对User对象进行自定义格式设置。

#注意到，User类的定义与常规的python类定义有所不同，缺少了接收传入参数的__init__()方法。是因为Declarative系统会自动接收与我们在column中映射的名字匹配的关键字参数。

>>> User.__table__ 
Table('users', MetaData(bind=None),
            Column('id', Integer(), table=<users>, primary_key=True, nullable=False),
            Column('name', String(), table=<users>),
            Column('fullname', String(), table=<users>),
            Column('password', String(), table=<users>), schema=None)
#重点关注元数据MetaData
#Table对象是MetaData（一个更大的集合）的一部分。所以在使用Declarative时，就可以通过declarative基类的.metadata属性访问该对象。
#MetaData是一个注册表，它能向数据库发出有限的模式生产命令。该例中，我们的SQLite数据库实际上还没有一个叫users的表，但我们可以通过MetaData对数据库发出CREATE TABLE语句。

>>> Base.metadata.create_all(engine)
SELECT ...
PRAGMA table_info("users")
()
CREATE TABLE users (
    id INTEGER NOT NULL, name VARCHAR,
    fullname VARCHAR,
    password VARCHAR,
    PRIMARY KEY (id)
)
()
COMMI
#调用了MetaData.create_all()方法，将Engine对象作为一个数据库连接的来源传入。

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
#先有数据库连接的engine,再创建会话
Session = sessionmaker()

Seesion.configure(bind=engine)
#先创建会话，再与engine绑定

session = Session()
#会话初始化
#如果把database比作厨房的话，session只是一个盘子，操作的对象才是食物。

>>> ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
>>> session.add(ed_user)
#添加或者更新对象

>>> our_user = session.query(User).filter_by(name='ed').first() 
>>> our_user
<User(name='ed', fullname='Ed Jones', password='edspassword')>

>>> session.add_all([
...     User(name='wendy', fullname='Wendy Williams', password='foobar'),
...     User(name='mary', fullname='Mary Contrary', password='xxg527'),
...     User(name='fred', fullname='Fred Flinstone', password='blah')])
#一次性添加多个对象

ed_user.password = 'f8s7ccs'
#也可直接更改属性的值

>>> session.dirty
IdentitySet([<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>])
#dirty方法查看更改的对象

>>> session.new  
IdentitySet([<User(name='wendy', fullname='Wendy Williams', password='foobar')>,
<User(name='mary', fullname='Mary Contrary', password='xxg527')>,
<User(name='fred', fullname='Fred Flinstone', password='blah')>])
#查看新添加的对象


>>> session.commit()
#会话结束，提交所有tansaction

>>> ed_user.id 
1
#commit()之前为None的id属性变为了1.说明数据库中已经存在了ed_user这个记录。

>>> session.rollback()
#回滚到上一次commit()的状态。

query方法1
>>> for instance in session.query(User).order_by(User.id):
...     print(instance.name, instance.fullname)
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flinstone
#查询 query()方法返回一个Query对象
#上面的例子将Query对象放入一个可迭代的上下文即for循环中，最终返回了一个User对象的列表。

query方法2
>>> for name, fullname in session.query(User.name, User.fullname):
...     print(name, fullname)
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flinstone
#query()方法也可以接受一个元组，当然返回结果也是元组形式。

query方法3
>>> for row in session.query(User, User.name).all():
...    print(row.User, row.name)
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')> ed
<User(name='wendy', fullname='Wendy Williams', password='foobar')> wendy
<User(name='mary', fullname='Mary Contrary', password='xxg527')> mary
<User(name='fred', fullname='Fred Flinstone', password='blah')> fred

query方法4
>>> for row in session.query(User.name.label('name_label')).all():
...    print(row.name_label)
ed
wendy
mary
fred
#label()标签的使用


>>> from sqlalchemy.orm import aliased
>>> user_alias = aliased(User, name='user_alias')

>>> for row in session.query(user_alias, user_alias.name).all():
...    print(row.user_alias)
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>
<User(name='wendy', fullname='Wendy Williams', password='foobar')>
<User(name='mary', fullname='Mary Contrary', password='xxg527')>
<User(name='fred', fullname='Fred Flinstone', password='blah')>
#表的别名

>>> for u in session.query(User).order_by(User.id)[1:3]:
...    print(u)
<User(name='wendy', fullname='Wendy Williams', password='foobar')>
<User(name='mary', fullname='Mary Contrary', password='xxg527')>
#通过python数组的切片实现查询的LIMIT和OFFSET。

>>> for name, in session.query(User.name).\
...             filter_by(fullname='Ed Jones'):
...    print(name)
ed

>>> for name, in session.query(User.name).\
...             filter(User.fullname=='Ed Jones'):
...    print(name)
ed
#注意filter_by()和filter()二者方法接受参数的区别。

>>> for user in session.query(User).\
...          filter(User.name=='ed').\
...          filter(User.fullname=='Ed Jones'):
...    print(user)
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>
#查询返回的Query对象是完全可再生的fully gemerative，即可以不断的迭代查询，查询一次返回一个新的Query对象。
#所以多次的 .filter()方法调用即可实现查询的AND。

常见的过滤操作符：
equals:
	query.filter(User.name == 'ed')
	
not equals:
	query.filter(User.name != 'ed')
	
LIKE:
	query.filter(User.name.like('%ed%'))
	
ILIKE (case-insensitive LIKE):
	query.filter(User.name.ilike('%ed%'))
	
IN:
	query.filter(User.name.in_(['ed', 'wendy', 'jack']))

	# works with query objects too:
	query.filter(User.name.in_(
		session.query(User.name).filter(User.name.like('%ed%'))
	))
	
NOT IN:
	query.filter(~User.name.in_(['ed', 'wendy', 'jack']))
	
IS NULL:
	query.filter(User.name == None)

	# alternatively, if pep8/linters are a concern
	query.filter(User.name.is_(None))
	
IS NOT NULL:
	query.filter(User.name != None)

	# alternatively, if pep8/linters are a concern
	query.filter(User.name.isnot(None))

AND:
	# use and_()
	from sqlalchemy import and_
	query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))
	
	# or send multiple expressions to .filter()
	query.filter(User.name == 'ed', User.fullname == 'Ed Jones')

	# or chain multiple filter()/filter_by() calls
	query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')
	
OR:
	from sqlalchemy import or_
	query.filter(or_(User.name == 'ed', User.name == 'wendy'))

MATCH:
	query.filter(User.name.match('wendy'))

查询中返回Lists和Scalars的方法：

all() returns a list:

first() applies a limit of one and returns the first result as a scalar:

one() fully fetches all rows, and if not exactly one object identity or composite row is present in the result, raises an error. With multiple rows found:

one_or_none() is like one(), except that if no results are found, it doesn’t raise an error; it just returns None. Like one(), however, it does raise an error if multiple results are found.

scalar() invokes the one() method, and upon success returns the first column of the row:


#查询中文本字符串的使用：
>>> from sqlalchemy import text
>>> for user in session.query(User).\
...             filter(text("id<224")).\
...             order_by(text("id")).all():
...     print(user.name)
ed
wendy
mary
fred

>>> session.query(User).filter(text("id<:value and name=:name")).\
...     params(value=224, name='fred').order_by(User.id).one()
<User(name='fred', fullname='Fred Flinstone', password='blah')>
#可以通过params()方法向text()方法中的关键字传递对应的键值。

也可以直接SQL语句查询：
>>> session.query(User).from_statement(
...                     text("SELECT * FROM users where name=:name")).\
...                     params(name='ed').all()
[<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>]

>>> stmt = text("SELECT name, id, fullname, password "
...             "FROM users where name=:name")
>>> stmt = stmt.columns(User.name, User.id, User.fullname, User.password)#格式化字符串
>>> session.query(User).from_statement(stmt).params(name='ed').all()
[<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>]

>>> stmt = text("SELECT name, id FROM users where name=:name")
>>> stmt = stmt.columns(User.name, User.id)
>>> session.query(User.id, User.name).\
...          from_statement(stmt).params(name='ed').all()#params()格式化字符串
[(1, u'ed')]


计数：
>>> session.query(User).filter(User.name.like('%ed')).count()
2

>>> from sqlalchemy import func
>>> session.query(func.count(User.name), User.name).group_by(User.name).all()
[(1, u'ed'), (1, u'fred'), (1, u'mary'), (1, u'wendy')]

>>> session.query(func.count('*')).select_from(User).scalar()
4

>>> session.query(func.count(User.id)).scalar()
4


建立表之间的Relationship：

>>> from sqlalchemy import ForeignKey
>>> from sqlalchemy.orm import relationship

>>> class Address(Base):
...     __tablename__ = 'addresses'
...     id = Column(Integer, primary_key=True)
...     email_address = Column(String, nullable=False)
...     user_id = Column(Integer, ForeignKey('users.id'))#表addresses中user_id必须是表users中的id
...
...     user = relationship("User", back_populates="addresses")#“双边关系”bidirectional relationship第一边，将addresses中的user字段与表User绑定
...
...     def __repr__(self):
...         return "<Address(email_address='%s')>" % self.email_address

>>> User.addresses = relationship(
...     "Address", order_by=Address.id, back_populates="user")#“双边关系”bidirectional relationship第二边，将User中的addresses字段与表Address绑定

>>> Base.metadata.create_all(engine)#通过metadata发出又一个CREATE（以在数据库中创建addresses表）

Related 对象的操作案例：
>>> jack = User(name='jack', fullname='Jack Bean', password='gjffdd')
>>> jack.addresses
[]
#设置relationship后，创建一个User就“自带”有addresses,只不过在这还未给addresses赋值，其返回值为空的List。

>>> jack.addresses = [
...                 Address(email_address='jack@google.com'),
...                 Address(email_address='j25@yahoo.com')]

>>> jack.addresses[1]
<Address(email_address='j25@yahoo.com')>

>>> jack.addresses[1].user
<User(name='jack', fullname='Jack Bean', password='gjffdd')>

>>> session.add(jack)
>>> session.commit()

>>> jack = session.query(User).\
... filter_by(name='jack').one()
>>> jack
<User(name='jack', fullname='Jack Bean', password='gjffdd')>

>>> jack.addresses
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]

联合查询：
>>> for u, a in session.query(User, Address).\
...                     filter(User.id==Address.user_id).\
...                     filter(Address.email_address=='jack@google.com').\
...                     all():
...     print(u)
...     print(a)
<User(name='jack', fullname='Jack Bean', password='gjffdd')>
<Address(email_address='jack@google.com')>

>>> session.query(User).join(Address).\
...         filter(Address.email_address=='jack@google.com').\
...         all()
[<User(name='jack', fullname='Jack Bean', password='gjffdd')>]
#query.join()方法

#当User与Address间没有foreign key时，可以用以下几种形式：
query.join(Address, User.id==Address.user_id)    # explicit condition
query.join(User.addresses)                       # specify relationship from left to right
query.join(Address, User.addresses)              # same, with explicit target
query.join('addresses')                          # same, using a string

query.outerjoin(User.addresses)#外连接

#使用aliased，可以join查询两次，以得到具有两不同email addresses的user：
>>> from sqlalchemy.orm import aliased
>>> adalias1 = aliased(Address)
>>> adalias2 = aliased(Address)
>>> for username, email1, email2 in \
...     session.query(User.name, adalias1.email_address, adalias2.email_address).\
...     join(adalias1, User.addresses).\
...     join(adalias2, User.addresses).\
...     filter(adalias1.email_address=='jack@google.com').\
...     filter(adalias2.email_address=='j25@yahoo.com'):
...     print(username, email1, email2)
jack jack@google.com j25@yahoo.com

子查询：
>>> from sqlalchemy.sql import func
>>> stmt = session.query(Address.user_id, func.count('*').\
...         label('address_count')).\
...         group_by(Address.user_id).subquery()

>>> for u, count in session.query(User, stmt.c.address_count).\
...     outerjoin(stmt, User.id==stmt.c.user_id).order_by(User.id):
...     print(u, count)
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')> None
<User(name='wendy', fullname='Wendy Williams', password='foobar')> None
<User(name='mary', fullname='Mary Contrary', password='xxg527')> None
<User(name='fred', fullname='Fred Flinstone', password='blah')> None
<User(name='jack', fullname='Jack Bean', password='gjffdd')> 2
#  .c的使用，即.column

>>> stmt = session.query(Address).\
...                 filter(Address.email_address != 'j25@yahoo.com').\
...                 subquery()
>>> adalias = aliased(Address, stmt)
>>> for user, address in session.query(User, adalias).\
...         join(adalias, User.addresses):
...     print(user)
...     print(address)
<User(name='jack', fullname='Jack Bean', password='gjffdd')>
<Address(email_address='jack@google.com')>

>>> from sqlalchemy.sql import exists
>>> stmt = exists().where(Address.user_id==User.id)
>>> for name, in session.query(User.name).filter(stmt):
...     print(name)
jack
#exists()方法

>>> for name, in session.query(User.name).\
...         filter(User.addresses.any()):
...     print(name)
jack
#any()
>>> for name, in session.query(User.name).\
...     filter(User.addresses.any(Address.email_address.like('%google%'))):
...     print(name)
jack

>>> session.query(Address).\
...         filter(~Address.user.has(User.name=='jack')).all()
[]
#has()

Relationship操作符：
contains() (used for one-to-many collections):

	query.filter(User.addresses.contains(someaddress))
	
has() (used for scalar references):

	query.filter(Address.user.has(name='ed'))

Query.with_parent() (used for any relationship):

	session.query(Address).with_parent(someuser, 'addresses')

Sqlalchemy提供了三种eager loading，通过query.options()函数实现。
1. subquery load:
>>> from sqlalchemy.orm import subqueryload
>>> jack = session.query(User).\
...                 options(subqueryload(User.addresses)).\
...                 filter_by(name='jack').one()
>>> jack
<User(name='jack', fullname='Jack Bean', password='gjffdd')>

>>> jack.addresses
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]
	
2. 	joined load
>>> from sqlalchemy.orm import joinedload

>>> jack = session.query(User).\
...                        options(joinedload(User.addresses)).\
...                        filter_by(name='jack').one()
>>> jack
<User(name='jack', fullname='Jack Bean', password='gjffdd')>

>>> jack.addresses
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]
	
3. explicit join + eagerlaod	
>>> from sqlalchemy.orm import contains_eager
>>> jacks_addresses = session.query(Address).\
...                             join(Address.user).\
...                             filter(User.name=='jack').\
...                             options(contains_eager(Address.user)).\
...                             all()
>>> jacks_addresses
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]

>>> jacks_addresses[0].user
<User(name='jack', fullname='Jack Bean', password='gjffdd')>
	

删除操作：
>>> session.delete(jack)
>>> session.query(User).filter_by(name='jack').count()
0
>>> session.query(Address).filter(
...     Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
...  ).count()
2	
#删除user的jack记录后，其address仍然存在。。	

#要想改变现状，即删除jack记录时其address被一并删除，则需要在定义User.addresses双边关系时配置cascade options。
#所以，需要先删除前文已建立的relationship,彻底拆除映射关系后重新定义，具体操作如下：
>>> session.close()
ROLLBACK

>>> Base = declarative_base()#重新得到一个基类

>>> class User(Base):
...     __tablename__ = 'users'
...
...     id = Column(Integer, primary_key=True)
...     name = Column(String)
...     fullname = Column(String)
...     password = Column(String)
...
...     addresses = relationship("Address", back_populates='user',
...                     cascade="all, delete, delete-orphan")#重点！！！
...
...     def __repr__(self):
...        return "<User(name='%s', fullname='%s', password='%s')>" % (
...                                self.name, self.fullname, self.password)
	
>>> class Address(Base):
...     __tablename__ = 'addresses'
...     id = Column(Integer, primary_key=True)
...     email_address = Column(String, nullable=False)
...     user_id = Column(Integer, ForeignKey('users.id'))
...     user = relationship("User", back_populates="addresses")
...
...     def __repr__(self):
...         return "<Address(email_address='%s')>" % self.email_address	

# load Jack by primary key
SQL>>> jack = session.query(User).get(5)

# remove one Address (lazy load fires off)
SQL>>> del jack.addresses[1]

# only one address remains
SQL>>> session.query(Address).filter(
...     Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
... ).count()
1

>>> session.delete(jack)

SQL>>> session.query(User).filter_by(name='jack').count()
0

SQL>>> session.query(Address).filter(
...    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
... ).count()
0
#删除jack时其address被一并删除了。

多对多关系的建立：
#以下是博客应用中的多对多关系案例：
>>> from sqlalchemy import Table, Text
>>> # association table
>>> post_keywords = Table('post_keywords', Base.metadata,
...     Column('post_id', ForeignKey('posts.id'), primary_key=True),
...     Column('keyword_id', ForeignKey('keywords.id'), primary_key=True)
... )
#创建一个不包含映射关系的表，该表只用来表征多对多关系。

>>> class BlogPost(Base):
...     __tablename__ = 'posts'
...
...     id = Column(Integer, primary_key=True)
...     user_id = Column(Integer, ForeignKey('users.id'))
...     headline = Column(String(255), nullable=False)
...     body = Column(Text)
...
...     # many to many BlogPost<->Keyword
...     keywords = relationship('Keyword',
...                             secondary=post_keywords,#将表post_keywords作为关系表
...                             back_populates='posts')
...
...     def __init__(self, headline, body, author):
...         self.author = author
...         self.headline = headline
...         self.body = body
...
...     def __repr__(self):
...         return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)


>>> class Keyword(Base):
...     __tablename__ = 'keywords'
...
...     id = Column(Integer, primary_key=True)
...     keyword = Column(String(50), nullable=False, unique=True)
...     posts = relationship('BlogPost',
...                          secondary=post_keywords,#将表post_keywords作为关系表
...                          back_populates='keywords')
...
...     def __init__(self, keyword):
...         self.keyword = keyword

#至此，BlogPost和keywords的多对多关系已经定义好了，下一步，想向BlogPost中添加author字段，并定义其与posts的双边关系（即一位作者可以由多篇文章，但一篇文章只有一位作者）：
>>> BlogPost.author = relationship(User, back_populates="posts")
>>> User.posts = relationship(BlogPost, back_populates="author", lazy="dynamic")#lazy关键字可以配置一可选择的属性加载策略loader strategy

>>> Base.metadata.create_all(engine)

>>> wendy = session.query(User).\
...                 filter_by(name='wendy').\
...                 one()
>>> post = BlogPost("Wendy's Blog Post", "This is a test", wendy)
>>> session.add(post)

>>> post.keywords.append(Keyword('wendy'))
>>> post.keywords.append(Keyword('firstpost'))

>>> session.query(BlogPost).\
...             filter(BlogPost.keywords.any(keyword='firstpost')).\
...             all()
[BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', password='foobar')>)]
#使用any()操作符来定位

>>> session.query(BlogPost).\
...             filter(BlogPost.author==wendy).\
...             filter(BlogPost.keywords.any(keyword='firstpost')).\
...             all()
[BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', password='foobar')>)]	
#查找作者是wendy,关键字有firstpost的post

>>> wendy.posts.\
...         filter(BlogPost.keywords.any(keyword='firstpost')).\
...         all()
[BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', password='foobar')>)]	
#利用wendy与posts间的动态关系,直接连续就地查询。
	
	

