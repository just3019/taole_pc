import json
import time

import requests

# 设置每页拉取40个商品
from base import printf
from taole import feedbacks

pagesize = 20


# 获取商品信息（获取不到价格）
def sn_search(keyword, lowprice, highprice, page=0):
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
        ('ps', pagesize),
        ('set', '5'),
        ('cf', '%s_%s' % (lowprice, highprice)),
        ('st', '9'),  # st:排序   9：价格升序  10：价格倒序  0：综合排序 8：销量排序
        ('cp', page)
    )
    snUrl = 'https://search.suning.com/emall/mobile/clientSearch.jsonp'
    response = requests.get(snUrl, headers=headers, params=params, timeout=2)
    # printf("苏宁：" + response.text)
    return json.loads(response.text)


# 获取商品价格
def get_sn_price(codes):
    headers = {
        'Host': 'ds.suning.com',
        'hiro_trace_type': 'SDK',
        'Accept': '*/*',
        'User-Agent': '\xE8\x8B\x8F\xE5\xAE\x81\xE6\x98\x93\xE8\xB4\xAD 7.4.2 rv:7.4.2.3 (iPhone; iOS 12.1.2; zh_CN) SNCLIENT',
        'sn_page_source': '',
        'Accept-Language': 'zh-Hans;q=1',
    }
    url = "https://ds.suning.com/ds/generalForTile/%s-571_571---322--.json" % codes
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def sn_search_list(keyword, lowprice, highprice, taskId=0):
    feedback_list = []
    page = 0
    try:
        while True:
            codes = ""
            beans = {}
            result = sn_search(keyword, lowprice, highprice, page)
            goods = result["goods"]
            for g in goods:
                codes += "%s__2_%s," % (g["catentryId"], g["salesCode10"])
                code = "%s" % g["catentryId"]
                codeR = code.zfill(18)
                id = "%s-%s" % (g["salesCode10"], g["catentryId"])
                name = g["catentdesc"]
                url = "https://product.suning.com/%s/%s.html" % (g["salesCode10"], g["catentryId"])
                dict = {"taskId": taskId, "url": url, "name": name, "productId": id}
                beans.update({codeR: dict})
            prices = get_sn_price(codes)["rs"]
            for p in prices:
                price = p["price"]
                originalPrice = p["originalPrice"] if (p["originalPrice"] != "") else price
                code = p["cmmdtyCode"]
                pr = {"lowPrice": price, "price": price, "originalPrice": originalPrice}
                beans[code].update(pr)
            for key in beans:
                feedback_list.append(beans[key])
                # 当商品数大于1000，则在1000的时候先发送服务器
                if len(feedback_list) == 1000:
                    params = {"feedbacks": feedback_list}
                    p = json.dumps(params)
                    printf(p)
                    feedbacks(p)
                    feedback_list = []
            time.sleep(1)
            if len(goods) != pagesize:
                break
            page += 1
        params = {"feedbacks": feedback_list}
        p = json.dumps(params)
        # printf(p)
        feedbacks(p)
    except RuntimeError as e:
        print("错误：%s" % e)


if __name__ == '__main__':
    sn_search_list("三星电视55寸", 1000, 9999, 6)
