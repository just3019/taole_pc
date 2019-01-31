import json
import time

import requests

from base import printf
from taole import feedbacks

headers = {
    'Host': 'mobile.gome.com.cn',
    'user-agent': 'iphone GomePlus 128.0.1;',
    'accept-language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    'accept': '*/*',
    'content-type': 'application/x-www-form-urlencoded',
}

params = (
    ('from', 'app_plus'),
)

gmUrl = "https://mobile.gome.com.cn/mobile/p/wapSearch.jsp"

pagesize = 20


def gm_search(keyword, lowprice, highprice, page=1):
    body = {
        "currentPage": page,
        "market": "20",
        "version": 2,
        "channel": 0,
        "merchantId": "",
        "crossShop": "",
        "searchType": 0,
        "keyWord": keyword,
        "price": "%sx%s" % (lowprice, highprice),
        "reqType": "0",
        "searchMode": "history",
        "priceTag": 1,
        "sortBy": 7,
        "extraWord": "",
        "shoppingCartActivityId": "",
        "regionID": "11010200"
    }
    data = 'body=' + json.dumps(body)
    # print(data)
    response = requests.post(gmUrl, headers=headers, params=params, data=data)
    # printf(response.text)
    return json.loads(response.text)


def gm_search_list(keyword, lowprice, highprice, taskId=0):
    feedback_list = []
    page = 1
    fail_count = 0
    try:
        while True:
            result = gm_search(keyword, lowprice, highprice, page)
            goods = result["goodsList"]
            for g in goods:
                if "goodsName" not in g:
                    continue
                id = "%s-%s" % (g["goodsNo"], g["skuID"])
                name = g["goodsName"]
                price = g["lowestSalePrice"]
                originalPrice = g["highestSalePrice"]
                url = "https://item.gome.com.cn/%s.html" % id
                price_dict_list = []
                price_dict = {"price": price}
                price_dict_list.append(price_dict)
                dict = {"taskId": taskId, "url": url, "lowPrice": price, "price": price, "originalPrice": originalPrice,
                        "name": name, "productId": id, "feedbackPrices": price_dict_list}
                # printf(dict)
                feedback_list.append(dict)
            time.sleep(3)
            totalCount = result["pageBar"]["totalCount"]
            # printf("totalCount：%s" % totalCount)
            # printf(totalCount == 0)
            if len(goods) != pagesize or fail_count > 5:
                break
            if totalCount == 0:
                fail_count += 1
                printf("fail_count：%s" % fail_count)
                continue
            page += 1
            # printf(page)
        params = {"feedbacks": feedback_list}
        p = json.dumps(params)
        # printf(p)
        feedbacks(p)
        # write("gm-%s%s.log" % (keyword, time.strftime("%Y%m%d")), "%s\n" % p)
    except RuntimeError as e:
        printf("错误：%s" % e)


if __name__ == '__main__':
    # gm_search("iphonexsmax", 6000, 10000)
    index = 1
    while True:
        printf("第%s任务" % index)
        gm_search_list("iphonexsmax", 6000, 10000)
        index += 1
