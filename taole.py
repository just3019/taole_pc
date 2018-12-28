import requests


def feedbacks(params):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url="http://taole.luckygrra.com/task/feedbacks", data=params, headers=headers)
    # response = requests.post(url="http://localhost:21000/task/feedbacks", data=params, headers=headers)
    # result = json.loads(response.text)
    # if "status" in response.text:
    #     if result["status"] == 1000:
    #         return True
    #     else:
    #         return False
    # else:
    #     time.sleep(10)
