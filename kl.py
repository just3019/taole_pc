import json
import time

import requests

from base import printf, write
from taole import feedbacks

headers = {
    'Host': 'gw.kaola.com',
    # '__oto__': '15',
    'user-agent': 'HTSpring/4.4.5 (iPhone; iOS 12.1.2; Scale/3.00)',
    # 'fromnative': '1',
    # 'deviceudid': '98858883c5791344c229a9a7d760e1d13efbe5f1',
    'appversion': '4.4.5',
    # 'appchannel': '1',
    # 'appsystemversion': '12.1.2',
    'version': '40405',
    'platform': '2',
    'devicemodel': 'iPhone9,2',
    'accept-language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    'apiversion': '208',
    # 'uiupdateswitch': '{"cart420AbTest":"1","appHomeAbtestSwitch":"1","appSearchBarAbtestSwitch":"1","appSearchNavAbtestSwitch":"1","appGoodsDetailAbtestSwitch":"1","appCartAbtestSwitch":"1"}',
    'accept': 'application/json',
    'content-type': 'application/json;charset=UTF-8',
}

paramsKL = (
    ('version', '1.0'),
)

pagesize = 100


def kl_search(keyword, lowprice, highprice, page=1):
    data = {
        "search": {
            "isFilter": 0,
            "isSearch": 1,
            "stock": 0,
            "key": keyword,
            "shownActivityNum": -1,
            "spellCheck": 1,
            "filterTypeList": [{
                "type": 2,
                "priceRanges": [{
                    "highPrice": highprice,
                    "lowPrice": lowprice
                }]
            }]
        },
        "pageSize": pagesize,
        "pageNo": page
    }
    klurl = 'https://gw.kaola.com/gw/search/list/goods'
    response = requests.post(klurl, headers=headers, params=paramsKL, data=json.dumps(data))
    # printf("考拉：" + response.text)
    return json.loads(response.text)


def kl_search_list(keyword, lowprice, highprice, taskId=0):
    feedback_list = []
    page = 1
    try:
        while True:
            result = kl_search(keyword, lowprice, highprice, page)
            goods = result["body"]["result"]["itemList"]
            for g in goods:
                if "goodsModuleItem" not in g:
                    continue
                gg = g["goodsModuleItem"]
                id = gg["goodsId"]
                name = gg["title"]
                price = gg["stringPrice"]
                originalPrice = gg["originalPrice"]
                url = "https://goods.kaola.com/product/%s.html" % id
                price_dict_list = []
                price_dict = {"price": price}
                price_dict_list.append(price_dict)
                dict = {"taskId": taskId, "url": url, "lowPrice": price, "price": price, "originalPrice": originalPrice,
                        "name": name, "productId": id, "feedbackPrices": price_dict_list}
                # printf(dict)
                feedback_list.append(dict)
            time.sleep(1)
            if len(goods) != pagesize:
                break
            page += 1
        params = {"feedbacks": feedback_list}
        p = json.dumps(params)
        # printf(p)
        feedbacks(p)
        write("kl-%s%s.log" % (keyword, time.strftime("%Y%m%d")), "%s\n" % p)
    except RuntimeError as e:
        printf("错误：%s" % e)


def kl_deal(keyword, lowprice, highprice, num):
    try:
        t = time.time()
        for i in range(0, num):
            kl_search_list(keyword, lowprice, highprice)
            time.sleep(10)
        t1 = time.time()
        printf("本次任务完成 %s" % (t1 - t))
    except RuntimeError as e:
        print(e)


if __name__ == '__main__':
    kl_search_list("iphone", 100, 10000)
    # key = input("输入搜索的关键字：")
    # count = eval(input("创建几个任务："))
    # num = eval(input("一个任务循环多少次："))
    # t = time.time()
    # Tp = ThreadPool(1)
    # for i in range(0, count):
    #     printf("执行第%s轮任务" % i)
    #     Tp.add_task(kl_deal, key, num)
    # Tp.wait_completion()
    # printf(time.time() - t)
