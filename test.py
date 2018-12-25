import sn

# headers = {
#     'Host': 'search.suning.com',
#     'hiro_trace_type': 'SDK',
#     'Accept': '*/*',
#     'User-Agent': '\xE8\x8B\x8F\xE5\xAE\x81\xE6\x98\x93\xE8\xB4\xAD 7.2.2 rv:7.2.2.5 (iPhone; iOS 12.1; zh_CN) SNCLIENT',
#     'sn_page_source': '',
#     'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
# }
# params = (
#     ('ct', "-1"),  # ct:是否苏宁服务  -1：非    2：是
#     ('keyword', "西门子冰箱"),
#     ('ps', '20'),
#     ('set', '5'),
# )
# response = requests.get('https://search.suning.com/emall/mobile/clientSearch.jsonp', headers=headers,
#                         params=params)
# print(response.text)

if __name__ == '__main__':
    sn.sn_search_list("macbookpro15英寸")
