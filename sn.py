import time

import requests

from base import printf


def sn_search_list(keyword):
    try:
        headers = {
            'Host': 'search.suning.com',
            'hiro_trace_type': 'SDK',
            'Accept': '*/*',
            'User-Agent': '\xE8\x8B\x8F\xE5\xAE\x81\xE6\x98\x93\xE8\xB4\xAD 7.2.2 rv:7.2.2.5 (iPhone; iOS 12.1; zh_CN) SNCLIENT',
            'sn_page_source': '',
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
        }
        params = (
            ('ct', "-1"),  # ct:是否苏宁服务  -1：非    2：是
            ('keyword', keyword),
            ('ps', '20'),
            ('set', '5'),
        )
        response = requests.get('https://search.suning.com/emall/mobile/clientSearch.jsonp', headers=headers,
                                params=params)
        print(response.text)
        return response.text
    except RuntimeError as e:
        print("错误：%s" % e)


def sn_search_list_thread(keyword, num):
    global driver
    try:
        t = time.time()
        for i in range(0, num):
            sn_search_list(keyword)
        t1 = time.time()
        printf("本次任务完成 %s" % (t1 - t))
    except RuntimeError as e:
        print(e)
