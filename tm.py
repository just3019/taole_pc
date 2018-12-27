import requests

response = requests.get(
    "https://list.tmall.com/search_product.htm?q=iphonexsmax&start_price=2000&end_price=10000&sort=p")
print(response.text)
