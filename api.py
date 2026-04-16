import requests
import json

url = 'https://innoflow.study.sensetime.com/v1/apiserver/facial-expression'
def facial_expression(path:str):
    files = {
        'file': open(path, 'rb')
    }

    response = requests.post(url, files=files)
    if response.status_code != 200:
        return None,f"request error: {response.status_code},resp: {response.text}"
    resp = response.json()
    emotion = resp[0]['dominant_emotion']
    return emotion,None

