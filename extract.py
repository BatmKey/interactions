from lxml import etree
from handler.read_format import number_format


def is_exist(body):
    invalid_content = ['页面不存在', '抱歉']
    for each in invalid_content:
        if each in body:
            return False
    return True


def extract_item(url, html_source):
    """根据链接判定平台获取字段
    Args:
        url ([string]): [链接]
        html_source ([string]): [网页源码]
    returns: dict
    """
    read_num = ''
    fans_num = ''
    gentie_num = ''
    comment_num = ''
    for site in sites_config:
        if site['domain'] in url:
            html = etree.HTML(html_source)
            config = site['config']
            # 判断是否key是否存在，存在则去取 xpath 提取内容
            read_num = number_format(''.join(html.xpath(config['read_num']))) \
                if config.get('read_num', '') else ''
            fans_num = number_format(''.join(html.xpath(config['fans_num']))) \
                if config.get('fans_num', '') else ''
            gentie_num = number_format(''.join(html.xpath(config['gentie_num']))) \
                if config.get('gentie_num', '') else ''
            comment_num = number_format(''.join(html.xpath(config['read_num']))) \
                if config.get('comment_num', '') else ''
    result = {
        'url': url,
        'read_num': read_num,
        'fans_num': fans_num,
        'gentie_num': gentie_num,
        'comment_num': comment_num
    }
    return result


sites_config = [
    {
        "site_name": "b站视频",
        "domain": "bilibili.com",
        "page_type": 1,
        "config": {
            "read_num": "//div[@class='video-data']/span[@class='view']/@title"
        }
    },
    {
        "site_name": "优酷视频",
        "domain": "youku.com",
        "page_type": 1,
        "config": {
            "fans_num": "//span[@class='subtitle ellipsis-style']/text()"
        }
    },
    {
        "site_name": "趣头条视频",
        "domain": "www.qctt.cn",
        "page_type": 1,
        "config": {
            "read_num": '//div[@class="author-info"]/span[@class="item"][2]/text()'
        }
    },
    {
        "site_name": "好看视频",
        "domain": "haokan.baidu.com",
        "page_type": 1,
        "config": {
            "read_num": '//div[@class="videoinfo-playnums"]/text()'
        }
    },
    {
        "site_name": "凤凰视频",
        "domain": "v.ifeng.com",
        "page_type": 1,
        "config": {
            "read_num": '//span[@class="playNum-F2CvXOAB"]//text()'
        }
    },
    {
        "site_name": "afcun视频",
        "domain": "www.acfun.cn",
        "page_type": 1,
        "config": {
            "read_num": '//span[@class="viewsCount"]/text()'
        }
    },
    {
        "site_name": "网易跟帖",
        "domain": "www.163.com",
        "page_type": 1,
        "config": {
            "gentie_num": '//a[@statistic="GTnews_top_tieCount"]/text()',
            "comment_num": '//a[@statistic="GTnews_top_tieJion"]/text()'
        }
    }
]
