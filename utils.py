import requests
from selenium import webdriver
# import json


# SPLASH_API = 'http://112.253.2.6:8060/execute'

# def getsource(url, page_type=0):
#     """
#     传入url获取网页源码
#     page_type: 1 -> 动态页面需要js加载
#     0 -> 静态页面不需要js加载
#     """
#     headers = {
#      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
#                    'Chrome/91.0.4472.77 Safari/537.36 '
#     }
#     if page_type == 0:
#         response = requests.get(url, headers=headers).content
#     else:
      
#     return response




# driver.set_window_size(1120, 550)



#  payload = json.dumps({
#           "url": url,
#           "wait": 1,
#           "resource_timeout": 0,
#           "viewport": "1024x768",
#           "render_all": False,
#           "images": 1,
#           "http_method": "GET",
#           "html5_media": False,
#           "http2": False,
#           "save_args": [],
#           "load_args": {},
#           "timeout": 90,
#           "request_body": False,
#           "response_body": False,
#           "engine": "webkit",
#           "har": 0,
#           "png": 1,
#           "html": 1,
#           "lua_source": "function main(splash, args)\r\n  assert(splash:go(args.url))\r\n  assert(splash:wait("
#                         "0.5))\r\n  return {\r\n    html = splash:html(),\r\n    png = splash:png(),\r\n    har = "
#                         "splash:har(),\r\n  }\r\nend "
#         })
#         headers = {
#           'Content-Type': 'application/json'
#         }
#         response = requests.request("POST", SPLASH_API, headers=headers, data=payload).content