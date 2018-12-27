import requests

headers = {
    'authority': 's.taobao.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
}

params = (
    ('q', 'iphone'),
    ('ie', 'utf8'),
    ('filter', 'reserve_price[5000,10000]'),
    ('sort', 'price-asc'),
)

response = requests.get('https://s.taobao.com/search', headers=headers, params=params)
print(response.text)
