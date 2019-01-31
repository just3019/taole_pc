import json
import time

import requests
from bs4 import BeautifulSoup

from taole import feedbacks

headers = {
    'authority': 'search.jd.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'referer': 'https://search.jd.com/Search?keyword=%E8%8D%A3%E8%80%80Note10&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E8%8D%A3%E8%80%80Note10&page=3&s=61&click=0',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
}

s = requests.session()
offset = 0


# 搜索第一次请求
def jd_search(keyword, lowprice, highprice):
    params = (
        ('keyword', keyword),
        ('enc', 'utf-8'),
        ('qrst', '1'),
        ('rt', '1'),
        ('stop', '1'),
        ('vt', '2'),
        ('ev', "exprice_%s-%s^" % (lowprice, highprice)),
        ('uc', '0'),
    )
    r = s.get('https://search.jd.com/search', headers=headers, params=params)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    # gl_list = soup.find_all("li", class_="gl-item")
    # for gl in gl_list:
    #     # print(gl)
    #     nameHTML = gl.find_all("em")
    #     nameSize = len(nameHTML)
    #     print(nameSize)
    #     name = ""
    #     for i in range(1, nameSize):
    #         name += nameHTML[i].text
    #     price = gl.find("strong").find("i").text
    #     # if name == "":
    #     #     print(gl)
    #     print(name + "\n" + price)
    return soup.find_all("li", class_="gl-item")


# 每一页往下加载
def jd_search_s(keyword, lowprice, highprice, page=1):
    params = (
        ('keyword', keyword),
        ('enc', 'utf-8'),
        ('qrst', '1'),
        ('rt', '1'),
        ('stop', '1'),
        ('vt', '2'),
        ('ev', "exprice_%s-%s^" % (lowprice, highprice)),
        ('page', 2 * page),
        ('s', offset + 1),
        ('scrolling', 'y'),
        ('log_id', '%.5f' % time.time()),
        ('tpl', '3_M'),
    )
    r = s.get('https://search.jd.com/s_new.php', headers=headers, params=params)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup.find_all("li", class_="gl-item")


# 后续翻页请求
def jd_search_next(keyword, lowprice, highprice, page=1):
    params = (
        ('keyword', keyword),
        ('enc', 'utf-8'),
        ('qrst', '1'),
        ('rt', '1'),
        ('stop', '1'),
        ('vt', '2'),
        ('ev', "exprice_%s-%s^" % (lowprice, highprice)),
        ('page', (2 * page - 1)),
        ('s', offset + 1),
        ('click', '0'),
    )
    r = s.get('https://search.jd.com/s_new.php', headers=headers, params=params)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup.find_all("li", class_="gl-item")


def jd_new_search_list(keyword, lowprice, highprice, taskId=0):
    global offset
    offset = 0
    # 首页点击搜索进入
    first = jd_search(keyword, lowprice, highprice)
    offset = len(first)
    first_s = jd_search_s(keyword, lowprice, highprice)
    first.extend(first_s)
    offset += len(first_s)
    # 第2页开始进行翻页
    page = 2
    while True:
        # 下一页
        next_fan = jd_search_next(keyword, lowprice, highprice, page)
        offset += len(next_fan)
        if len(next_fan) == 0:
            break
        first.extend(next_fan)
        next_s = jd_search_s(keyword, lowprice, highprice, page)
        offset += len(next_s)
        if len(next_s) == 0:
            break
        first.extend(next_s)
        page += 1
        time.sleep(1)
    feedback_list = []
    for gl in first:
        id = gl.get("data-sku")
        nameHTML = gl.find_all("em")
        nameSize = len(nameHTML)
        name = ""
        for i in range(1, nameSize):
            name += nameHTML[i].text
        price = gl.find("strong").find("i").text
        originalPrice = price
        url = "http://item.jd.com/%s.html" % id
        price_dict_list = []
        price_dict = {"price": price}
        price_dict_list.append(price_dict)
        dict = {"taskId": taskId, "url": url, "lowPrice": price, "price": price, "originalPrice": originalPrice,
                "name": name, "productId": id, "feedbackPrices": price_dict_list}
        # printf(dict)
        feedback_list.append(dict)
        # 当商品数大于1000，则在1000的时候先发送服务器
        if len(feedback_list) == 1000:
            params = {"feedbacks": feedback_list}
            p = json.dumps(params)
            # printf(p)
            feedbacks(p)
            feedback_list = []
    params = {"feedbacks": feedback_list}
    p = json.dumps(params)
    # printf(p)
    feedbacks(p)


if __name__ == '__main__':
    k = "电视55寸,1000,10000"
    # kk = k.split("|")
    # for i in kk:
    #     r = i.split(",")
    #     keyword = r[0]
    #     lowprice = r[1]
    #     highprice = r[2]
    #     printf("执行keyword：%s" % keyword)
    #     jd_new_search_list(keyword, lowprice, highprice)
    jd_new_search_list("电视55寸", 1000, 1500)
