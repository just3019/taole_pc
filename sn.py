import json
import time

import requests

from base import printf
from taole import feedbacks

headers = {
    'Host': 'search.suning.com',
    'hiro_trace_type': 'SDK',
    'Accept': '*/*',
    'User-Agent': '\xE8\x8B\x8F\xE5\xAE\x81\xE6\x98\x93\xE8\xB4\xAD 7.2.2 rv:7.2.2.5 (iPhone; iOS 12.1; zh_CN) SNCLIENT',
    'sn_page_source': '',
    'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
}

pagesize = 40


def sn_search(keyword, lowprice, highprice, page=0):
    params = (
        ('ct', "-1"),  # ct:是否苏宁服务  -1：非    2：是
        ('keyword', keyword),
        ('ps', pagesize),
        ('set', '5'),
        ('cf', '%s_%s' % (lowprice, highprice)),
        ('st', '9'),  # st:排序   9：价格升序  10：价格倒序  0：综合排序 8：销量排序
        ('cp', page)
    )
    snUrl = 'https://search.suning.com/emall/mobile/clientSearch.jsonp'
    response = requests.get(snUrl, headers=headers, params=params, timeout=2)
    printf("苏宁：" + response.text)
    return json.loads(response.text)


def sn_search_list(keyword, lowprice, highprice, taskId=0):
    try:
        feedback_list = []
        page = 0
        while True:
            result = sn_search(keyword, lowprice, highprice, page)
            goods = result["goods"]
            for g in goods:
                id = "%s-%s" % (g["salesCode10"], g["catentryId"])
                name = g["catentdesc"]
                price = g["price"]
                originalPrice = price  # 原价
                url = "https://product.suning.com/%s/%s.html" % (g["salesCode10"], g["catentryId"])
                price_dict_list = []
                price_dict = {"price": price}
                price_dict_list.append(price_dict)
                dict = {"taskId": taskId, "url": url, "lowPrice": price, "price": price, "originalPrice": originalPrice,
                        "name": name, "productId": id, "feedbackPrices": price_dict_list}
                feedback_list.append(dict)
                # 当商品数大于1000，则在1000的时候先发送服务器
                if len(feedback_list) == 1000:
                    params = {"feedbacks": feedback_list}
                    p = json.dumps(params)
                    # printf(p)
                    feedbacks(p)
                    feedback_list = []
            time.sleep(2)
            if len(goods) != pagesize:
                break
            page += 1
        params = {"feedbacks": feedback_list}
        p = json.dumps(params)
        # printf(p)
        feedbacks(p)
    except RuntimeError as e:
        print("错误：%s" % e)


def sn_search_list_thread(keyword, lowprice, highprice, num):
    try:
        t = time.time()
        for i in range(0, num):
            sn_search_list(keyword, lowprice, highprice)
        t1 = time.time()
        printf("本次任务完成 %s" % (t1 - t))
    except RuntimeError as e:
        print(e)


if __name__ == '__main__':
    r = sn_search("三星电视55寸", 0, 9999)
    list = r["goods"]
    for g in list:
        id = "%s-%s" % (g["salesCode10"], g["catentryId"])
        code = "%s__2_%s" % (g["catentryId"], g["salesCode10"])
        name = g["catentdesc"]
        price = g["price"]
        url = "https://product.suning.com/%s/%s.html" % (g["salesCode10"], g["catentryId"])
        printf("%s" % code)
