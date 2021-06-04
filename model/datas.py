# coding=utf-8
from sqlalchemy import Column, Integer, String

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Datas(Base):
    __tablename__ = 'datas'
    # 各变量名一定要与表的各字段名一样，因为相同的名字是他们之间的唯一关联关系
    # 从语法上说，各变量类型和表的类型可以不完全一致，如表字段是String(64)，但我就定义成String(32)
    # 但为了避免造成不必要的错误，变量的类型和其对应的表的字段的类型还是要相一致
    # sqlalchemy强制要求必须要有主键字段不然会报错，如果要映射一张已存在且没有主键的表，那么可行的做法是将所有字段都设为primary_key=True
    # 不要看随便将一个非主键字段设为primary_key，然后似乎就没报错就能使用了，sqlalchemy在接收到查询结果后还会自己根据主键进行一次去重
    # 指定id映射到id字段; id字段为整型，为主键，自动增长（其实整型主键默认就自动增长）
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(256))
    # 指定name映射到name字段; name字段为字符串类形，
    # author_name = Column(String(256))
    # author_id = Column(String(256))
    like_num = Column(Integer)
    read_num = Column(Integer)
    fans_num = Column(Integer)
    comment_num = Column(Integer)
    gentie_num = Column(Integer)
    # # 1-文章 2-微头条 3-视频
    # types = Column(Integer)
    crawl_time = Column(Integer)
    is_del = Column(Integer)

    # __repr__方法用于输出该类的对象被print()时输出的字符串，如果不想写可以不写
    # def __repr__(self):
    #     return "<Data(url='%s', like_num='%s', read_num='%s')>" % (
    #         self.url, self.like_num, self.read_num)

# 视频类型 https://www.ixigua.com/6957721672602354213

# create table {
#     id int auto_increatment,
#     url varchar(255) NOT NULL,
#     author_name varchar(100) DEFAULT NULL,
#     author_id varchar(100) DEFAULT NULL,
#     like_num int DEFAULT NULL,
#     read_num int DEFAULT NULL,
#     comment_num int DEFAULT NULL,

#     crawl_time datetime DEFAULT CURRENT_TIMESTAMP,
#     is_del smallint DEFAULT 0,
#     primary key
# }
