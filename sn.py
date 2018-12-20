import json
import time

import requests

import base
from base import printf, write
from taole import feedbacks
from thread_pool import ThreadPool


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
        # print(response.text)
        result = json.loads(response.text)
        goods = result["goods"]
        feedback_list = []
        for g in goods:
            id = "%s-%s" % (g["salesCode10"], g["catentryId"])
            name = g["catentdesc"]
            price = g["price"]
            url = "https://product.suning.com/%s/%s.html" % (g["salesCode10"], g["catentryId"])
            price_dict_list = []
            price_dict = {"price": price}
            price_dict_list.append(price_dict)
            dict = {"url": url, "lowPrice": price, "price": price, "name": name, "productId": id,
                    "feedbackPrices": price_dict_list}
            # printf(dict)
            feedback_list.append(dict)
        params = {"feedbacks": feedback_list}
        p = json.dumps(params)
        # printf(p)
        feedbacks(p)
        write("sn-%s%s.log" % (keyword, time.strftime("%Y%m%d")), "%s\n" % params)
        return response.text
    except RuntimeError as e:
        print("错误：%s" % e)


def sn_search_list_thread(keyword, num):
    global driver
    try:
        t = time.time()
        for i in range(0, num):
            sn_search_list(keyword)
            time.sleep(10)
        t1 = time.time()
        printf("本次任务完成 %s" % (t1 - t))
    except RuntimeError as e:
        print(e)


if __name__ == '__main__':
    for i in range(0, 100):
        base.printf("执行第%s轮任务" % i)
        sn_search_list_thread("西门子冰箱", 100)
