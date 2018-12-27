import json
import time

import requests

from base import printf, write
from taole import feedbacks

headers = {
    'Host': 'search.suning.com',
    'hiro_trace_type': 'SDK',
    'Accept': '*/*',
    'User-Agent': '\xE8\x8B\x8F\xE5\xAE\x81\xE6\x98\x93\xE8\xB4\xAD 7.2.2 rv:7.2.2.5 (iPhone; iOS 12.1; zh_CN) SNCLIENT',
    'sn_page_source': '',
    'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
}


def sn_search_list(keyword, lowprice, highprice):
    try:
        params = (
            ('ct', "-1"),  # ct:是否苏宁服务  -1：非    2：是
            ('keyword', keyword),
            ('ps', '40'),
            ('set', '5'),
            ('cf', '%s_%s' % (lowprice, highprice)),
            ('st', '9'),  # st:排序   9：价格升序  10：价格倒序  0：综合排序 8：销量排序
        )
        snUrl = 'https://search.suning.com/emall/mobile/clientSearch.jsonp'
        response = requests.get(snUrl, headers=headers, params=params)
        # printf(response.text)
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
        time.sleep(1)
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
    sn_search_list("iphonexsmax", 2000, 10000)
    # key = input("输入搜索的关键字：")
    # count = eval(input("创建几个任务："))
    # num = eval(input("一个任务循环多少次："))
    # t = time.time()
    # Tp = ThreadPool(1)
    # for i in range(0, count):
    #     printf("执行第%s轮任务" % i)
    #     Tp.add_task(sn_search_list_thread, key, lowprice, highprice, num)
    # Tp.wait_completion()
    # printf(time.time() - t)
