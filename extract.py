import re
from lxml import etree
from handler.read_format import number_format
import requests


def is_exist(url, body):
    if requests.get(url).status_code in [404, 503]:
        return False
    elif '404' in url:
        return False
    invalid_content = ['页面不存在']
    for each in invalid_content:
        if each in body:
            return False
    return True


def extract_item(url, html_source, detail_page=False):
    """根据链接判定平台获取字段
    Args:
        detail_page: 是否需要去获取详情页获取信息, 默认不需要
        url ([string]): [链接]
        html_source ([string]): [网页源码]
    returns: dict
    """
    read_num = ''
    fans_num = ''
    gentie_num = ''
    comment_num = ''
    like_num = ''

    for site in sites_config:
        if site['domain'] in url:
            html = etree.HTML(html_source)
            config = site['config']

            # 如果还没有获取到详情页
            if not detail_page:
                if site.get('need_more_detail', ''):
                    # detail_url = html.xpath(site['need_more_detail'])
                    detail_url = re.search(site['need_more_detail'], html_source)
                    if detail_url:
                        detail_url = detail_url.group(1)
                    return dict({'need_more_detail': detail_url})
            # 判断是否key是否存在，存在则去取 xpath 提取内容
            try:
                read_num = number_format(''.join(html.xpath(config['read_num']))) \
                    if config.get('read_num', '') else ''
                fans_num = number_format(''.join(html.xpath(config['fans_num']))) \
                    if config.get('fans_num', '') else ''
                gentie_num = number_format(''.join(html.xpath(config['gentie_num']))) \
                    if config.get('gentie_num', '') else ''
                comment_num = number_format(''.join(html.xpath(config['comment_num']))) \
                    if config.get('comment_num', '') else ''
                like_num = number_format(''.join(html.xpath(config['like_num']))) \
                    if config.get('like_num', '') else ''
            except:
                print('这条链接提取内容出错 %s' % url)
    result = {
        'url': url,
        'read_num': read_num,
        'fans_num': fans_num,
        'gentie_num': gentie_num,
        'comment_num': comment_num,
        'like_num': like_num
    }
    return result


sites_config = [
    {
        "site_name": "b站视频",
        "domain": "bilibili.com",
        "config": {
            "read_num": "//div[@class='video-data']/span[@class='view']/@title"
        }
    },
    {
        "site_name": "优酷视频",
        "domain": "youku.com",
        "config": {
            "fans_num": "//span[@class='subtitle ellipsis-style']/text()"
        }
    },
    {
        "site_name": "趣头条视频",
        "domain": "www.qctt.cn",
        "config": {
            "read_num": '//div[@class="author-info"]/span[@class="item"][2]/text()'
        }
    },
    {
        "site_name": "好看视频",
        "domain": "haokan.baidu.com",
        "config": {
            "read_num": '//div[@class="videoinfo-playnums"]/text()'
        }
    },
    {
        "site_name": "凤凰视频",
        "domain": "v.ifeng.com",
        "config": {
            "read_num": '//span[@class="playNum-F2CvXOAB"]//text()'
        }
    },
    {
        "site_name": "afcun视频",
        "domain": "www.acfun.cn",
        "config": {
            "read_num": '//span[@class="viewsCount"]/text()'
        }
    },
    {
        "site_name": "网易跟帖",
        "domain": "www.163.com",
        "config": {
            "gentie_num": '//a[@statistic="GTnews_top_tieCount"]/text()',
            "comment_num": '//a[@statistic="GTnews_top_tieJion"]/text()'
        }
    },
    {
        "site_name": "爱奇艺",
        "domain": "www.iqiyi.com",
        "need_more_detail": '"profileUrl":"(.*?)"',
        "config": {
            "fans_num": '//li[contains(@class,"list-li")][3]/a/p[1]/text()',
            "like_num": '//li[contains(@class,"list-li")][4]/a/p[1]/text()'
        }
    },
    {
        "site_name": "西瓜视频",
        "domain": "www.ixigua.com",
        "config": {
            "read_num": '//p[@class="videoDesc__videoStatics"]/span[1]/text()[1]',
        }
    },
]
