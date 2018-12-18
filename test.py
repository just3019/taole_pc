import requests

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
    ('keyword', 'iphonexsmax'),
    ('ps', '20'),
    ('set', '5'),
)

response = requests.get('https://search.suning.com/emall/mobile/clientSearch.jsonp', headers=headers, params=params)
print(response.text)

# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# response = requests.get('https://search.suning.com/emall/mobile/clientSearch.jsonp?cf=&channelId=MOBILE&ci=&cityId=571&cp=0&ct=-1&istongma=1&iv=-1&keyword=iphonexsmax&operate=0&ps=10&sc=&sesab=ABAABABB&set=5&st=0&v=1.27', headers=headers, cookies=cookies)
