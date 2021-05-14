import json

import flask
from flask import Flask, request, jsonify

import audioUtils
import client
import serverUtils

app = Flask(__name__)
token = 'B*TyX&y7bDd5xLXYNw5iaN6X7%QAiqTQ#9nvtgMX3X2risrD64ew!*Q9*ky3PRvrSWYE6euykHycNzQqmViKo%XfoyTCSrJTFSUK*ycP2P$!Psn55iJT4@b4tdxw*XA!'  # test token (nothing private)


def check_api_key():
    token_given = request.headers.get('Authorization')
    if token_given != token_given:
        flask.abort(401)


def get_body(name):
    data = json.loads(request.data.decode('utf8'))
    if not isinstance(data, dict):
        data = json.loads(data)

    data = str(data[name])
    return data


def get_sentence_in_body(name):
    data = json.loads(str(request.data.decode('utf8')).replace('"', '\"').replace("\'", "'"))
    if not isinstance(data, dict):
        data = json.loads(data)

    data = str(data[name]).lower()
    return data


@app.route("/input", methods=['POST'])
def input_sentence():
    check_api_key()

    listen_for_seconds = int(get_body('listen_for_seconds'))
    speech_before_input = get_sentence_in_body('speech_before_input')
    return serverUtils.inputSentence(listen_for_seconds, speech_before_input)


@app.route("/speak", methods=['POST'])
def speak():
    check_api_key()

    speech = get_body('speech')
    client.speak(speech)
    return jsonify("OK")


@app.route("/record", methods=['POST'])
def record_microphone_and_send_back():
    check_api_key()

    record_for_seconds = int(get_body('record_for_seconds'))
    speech_before_input = get_sentence_in_body('speech_before_input')

    client.speak(speech_before_input)

    audioUtils.record(record_for_seconds)

    return serverUtils.send_file_to_server(audioUtils.filename)


if __name__ == '__main__':
    app.run(port=5001, debug=False, host='0.0.0.0', threaded=True)
