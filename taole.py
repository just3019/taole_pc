import json

import requests


def feedbacks(params):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url="http://taole.luckygrra.com/task/feedbacks", data=params, headers=headers)
    result = json.loads(response.text)
    if result["status"] == 1000:
        return True
    else:
        return False
