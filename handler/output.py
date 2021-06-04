# coding=utf-8
import time
from handler.csvWriterPy3 import CSVDumper
from model.datas import Datas


def write_by_ids(tasks, session):
    name = time.strftime("%Y-%m-%d#%H_%M_%S", time.localtime(int(time.time())))
    dumper = CSVDumper(f'{name}.csv')
    for task in tasks:
        data = session.query(Datas).filter_by(url=task[0]).order_by(Datas.crawl_time.desc()).first()
        if data:
            dumper.process_item(
                {
                    "3_链接": task[0],
                    "4_阅读数": data.read_num if data.read_num else -1,
                    "5_评论数": data.comment if data.comment else 0,
                    "6_点赞数": data.like if data.like else 0,
                    "1_作者id": data.author_id,
                    "2_类型": data.types,
                    "7_是否删帖": data.is_del,
                    "0_互动更新时间": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data.crawl_time))
                })
        else:
            dumper.process_item(
                {
                    "3_链接": task[0],
                    "4_阅读数": -1,
                    "5_评论数": -1,
                    "6_点赞数": -1,
                    "1_作者id": -1,
                    "2_类型": -1,
                    "7_是否删帖": "本地数据未查询(未抓取)到该条，请先扫描再导出",
                    "0_互动更新时间": "-"
                })

    print('导出数据完毕！')
    return f'{name}.csv'
