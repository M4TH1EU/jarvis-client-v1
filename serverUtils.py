import json

import requests
import speech_recognition as sr
from flask import jsonify
from requests.structures import CaseInsensitiveDict

# from client import no_voice_mode, speak
import client

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
        return "error"


def inputSentence(listen_for_seconds, speech_before_input):
    r = sr.Recognizer()

    try:
        if client.no_voice_mode:
            data = input("Entrez phrase : ").lower()
        else:
            with sr.Microphone(device_index=0) as source:
                r.adjust_for_ambient_noise(source=source, duration=0.5)
                client.speak(speech_before_input)
                audio = r.listen(source, timeout=3,
                                 phrase_time_limit=(listen_for_seconds if not client.no_voice_mode else 1))

            # now uses Google speech recognition
            data = r.recognize_google(audio, language="fr-FR")
            data = data.lower()  # makes all voice entries show as lower case

        print("DATA : " + data)
        return data

    except sr.UnknownValueError:
        client.speak(get_random_sentence_with_id('dontUnderstand'))
        return "Error"
    except sr.RequestError as e:  # if you get a request error from Google speech engine
        print(
            "Erreur du service Google Speech Recognition ; {0}".format(e))


def send_file_to_server(path):
    url_service = server_url + "/send_record"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "text/xml; charset=utf8"
    headers["Authorization"] = token

    data = open(path, 'rb').read()

    response = requests.post(url_service, headers=headers, data=data)
    return jsonify(json.loads(response.content))
