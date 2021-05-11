import json

import requests
from requests.structures import CaseInsensitiveDict

server_url = "http://127.0.0.1:5000"
token = 'B*TyX&y7bDd5xLXYNw5iaN6X7%QAiqTQ#9nvtgMX3X2risrD64ew!*Q9*ky3PRvrSWYE6euykHycNzQqmViKo%XfoyTCSrJTFSUK*ycP2P$!Psn55iJT4@b4tdxw*XA!'  # test token (nothing private)


def send_to_server(sentence):
    return callAPI('POST', '/send', {"sentence": sentence})


def get_random_sentence_with_id(sentence_id):
    return callAPI('POST', '/sentence/get_by_id', {"sentenceId": sentence_id})


def get_hotword():
    return callAPI(method='GET', url='/hotword')


def callAPI(method, url, json_data=None):
    if json_data is None:
        json_data = {}

    try:
        url_service = server_url + url

        headers = CaseInsensitiveDict()
        headers["Authorization"] = token
        headers["Content-Type"] = "application/json; charset=utf8"

        if method == 'GET':
            return json.loads(requests.get(url_service, headers=headers).content.decode("utf-8"))
        elif method == 'POST':
            json_data = json.dumps(json_data)
            return json.loads(
                requests.post(url_service, headers=headers, data=json_data.encode("utf8")).content.decode("utf-8"))
    except:
        print("Error when calling the server API")
