import json
import time

import requests

from base import printf, write
from taole import feedbacks

headers = {
    'Host': 'www.amazon.cn',
    'Accept': '*/*',
    'User-Agent': 'mShop:::Amazon_iPhone_11.21.2:::iPhone:::iPhone_OS_12.1.2',
    'Accept-Language': 'zh-cn',
}

pagesize = 40


def ymx_search(keyword, page):
    params = (
        ('rh', 'i:aps,k:%s' % keyword),
        ('sort', 'price-desc-rank'),
        ('keywords', keyword),
        ('ie', 'UTF8'),
        ('qid', int(time.time())),
        ('k', keyword),
        ('imgRes', '750'),
        ('dataVersion', 'v0.2'),
        ('format', 'json'),
        ('imgCrop', '1'),
        ('page', page),
        ('maxResults', pagesize),
        ('cid', '78466f529a8fb3ddf5af7b34217590254d9061224f75961eb3c25d28ee958170'),
    )

    response = requests.get('https://www.amazon.cn/s/ref=sr_st_price-desc-rank', headers=headers, params=params)
    # printf(response.text)
    return json.loads(response.text)


def ymx_search_list(keyword, lowprice, highprice, taskId=0):
    try:
        feedback_list = []
        page = 1
        tmp = 100000
        while True:
            result = ymx_search(keyword, page)
            goods = result["results"]["sections"][0]["items"]
            for g in goods:
                id = g["asin"]
                name = g["title"]
                if "buy" not in json.dumps(g):
                    continue
                price = g["prices"]["buy"]["price"].replace('￥', '').replace(',', '')
                tmp = int(float(price))
                if tmp > int(highprice):
                    continue
                if tmp < int(lowprice):
                    break
                originalPrice = price  # 原价
                url = "https://www.amazon.cn/dp/%s" % id
                price_dict_list = []
                price_dict = {"price": price}
                price_dict_list.append(price_dict)
                dict = {"taskId": taskId, "url": url, "lowPrice": price, "price": price, "originalPrice": originalPrice,
                        "name": name, "productId": id, "feedbackPrices": price_dict_list}
                # printf(dict)
                feedback_list.append(dict)
            time.sleep(1)
            if len(goods) != pagesize or tmp < int(lowprice):
                break
            page += 1
        params = {"feedbacks": feedback_list}
        p = json.dumps(params)
        # printf(p)
        feedbacks(p)
        write("ymx-%s%s.log" % (keyword, time.strftime("%Y%m%d")), "%s\n" % p)
    except RuntimeError as e:
        print("错误：%s" % e)


if __name__ == '__main__':
    # ymx_search("华为p20", 3)
    ymx_search_list("macbookpro", 10000, 18000)
