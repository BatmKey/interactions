# coding=utf-8
"""
基本逻辑
"""
import os
import time
import traceback
from shutil import copyfile
import random
from selenium import webdriver
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
import datetime
from handler.output import write_by_ids
from model.datas import Datas

from extract import extract_item, is_exist

CHOUR = 2
engine = create_engine('sqlite:///info.db')
if not engine.dialect.has_table(engine, 'datas'):
    metadata = sqlalchemy.schema.MetaData(engine)
    sqlalchemy.schema.Table('datas', metadata,
                            Column('id', Integer, primary_key=True, autoincrement=True),
                            Column('url', String(256)),
                            Column('like_num', Integer),
                            Column('read_num', Integer),
                            Column('fans_num', Integer),
                            Column('comment_num', Integer),
                            Column('gentie_num', Integer),
                            Column('crawl_time', Integer),
                            Column('is_del', Integer))
    metadata.create_all()
Session = sessionmaker(bind=engine)
session = Session()

# ed_user = Datas(aid=6957721672602354213, author_name="爱玩儿车EverCar", author_id="3724783485983447", types=3, read=8204,
#                 crawl_time=int(time.time()), comment=17)
# session.add(ed_user)
# session.commit()

"""
1.读取待处理数据
"""
with open('url.txt', 'r') as f:
    tasksr = f.readlines()

tasks = []

for task in tasksr:
    # 扫描所有的url作为task
    task = task.strip()
    if not task:
        continue
    tasks.append([task])

"""
1.5 选择动作
    1 - 开始扫描任务
    2 - 导出结果
"""

work = input("""
# 目前支持的平台有
### 视频类型 ###
1. b站 播放量
2. 优酷 粉丝数
3. 好看视频 播放量
4. afcun 播放量
5. 凤凰 播放量
6. 趣头条 播放量
7. 西瓜视频 播放量
8. 爱奇艺 用户名 粉丝数 点赞数

### 新闻类型
1. 网易新闻 跟帖数，评论数

# 请选择需要进行的操作，输入数字后回车
1. 【扫描】扫描获取互动数
2. 【导出】根据URL导出已抓取结果
3. 【删除全部缓存】将删除本地保存的全部缓存数据 - 一般不需要使用

--> 1 步骤可以反复执行，结果实时保存到本地数据库，失败可以直接重新运行。会自动继续执行。如果链接不变则2小时内不会重新跑作者页面会直接导出已抓到的数据。
--> 2 步骤会从本地数据库匹配提供的URL并导出数据
--> 3 步骤会将本地数据库删除并还原，平时不需要使用，仅在工具异常或者想重新跑(清理2小时缓存)时使用
--> 请输入：
""")
if int(work) == 2:
    ff = write_by_ids(tasks, session)
    print("【恭喜】全部任务已经完成，数据已经导出到", ff)
    print("请直接关闭")
    time.sleep(10000)
    exit(0)
if int(work) == 3:
    os.remove("info.db")
    copyfile(os.path.join('back_up', 'info.db'), 'info.db')
    print("清理成功，请直接退出 (5s)")
    time.sleep(5)
    exit(0)
"""
2. 记录所有url对应的账号id
"""
author_box = []
while True:
    # browser = webdriver.PhantomJS(executable_path='./phantomjs',
    #                               desired_capabilities=
    #                               {'phantomjs.page.settings.resourceTimeout': '10000',
    #                                'phantomjs.page.settings.userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
    #                                                                     'AppleWebKit/537.36 (KHTML, like Gecko) '
    rdm = random.randint(1000, 9999)
    rdm2 = random.randint(81, 91)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
    chrome_options.add_argument("disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--headless")
    browser = None
    try:
        browser = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)
    except:
        print("【错误】ChromeDriver 版本异常或者找不到！请退出")
        time.sleep(10000)
    browser.set_page_load_timeout(10)
    browser.set_script_timeout(10)
    browser.implicitly_wait(1)
    browser.set_window_size(1440, 660)
    for i, task in enumerate(tasks):
        # 查询是否已经抓取过, 并且没超时
        timestamp = int(time.mktime((datetime.datetime.now() - datetime.timedelta(hours=12)).timetuple()))
        data = session.query(Datas).filter_by(url=task[0]).filter(Datas.crawl_time > timestamp).first()
        try:
            if not data:
                print("进度条 -------", i, "/", len(tasks))
                browser.set_page_load_timeout(15)
                browser.get(task[0])
                body = browser.page_source
                time.sleep(1)
                browser.save_screenshot('1.png')
                # if "<body>error</body>" in body:
                #     # 已经被封 修改ua继续
                #     print("【被BAN·自动重启并继续】")
                #     browser.close()
                #     user_catch = False
                #     break
                if not is_exist(browser.current_url, body):
                    # 已删除
                    print('该帖子已经删除...自动跳过...%s' % task[0])
                    result = Datas(url=(task[0]), crawl_time=int(time.time()), is_del=1)
                    session.add(result)
                    session.commit()
                    continue
                item = extract_item(task[0], body)
                if item.get('need_more_detail', ''):
                    browser.get(item['need_more_detail'])
                    browser.save_screenshot('1.png')
                    body = browser.page_source
                    item = extract_item(task[0], body, detail_page=True)
                result = Datas(url=task[0],
                               read_num=item['read_num'],
                               fans_num=item['fans_num'],
                               comment_num=item['comment_num'],
                               gentie_num=item['gentie_num'],
                               like_num=item['like_num'],
                               crawl_time=int(time.time()),
                               is_del=0)
                session.add(result)
                session.commit()

            else:
                print("已经抓取过 %s 取数据库缓存" % task[0])
                continue
        except:
            print(traceback.format_exc())
            print('出现异常！ 重启继续')
            browser.close()
            break
    break

print("正在导出全部数据：")
ff = write_by_ids(tasks, session)
browser.close()
print("【恭喜】全部任务已经完成，数据已经导出到", ff)
print("请直接关闭")
time.sleep(10000)
