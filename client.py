import json
import struct
import sys
import threading
import time

import flask
import pvporcupine
import pyaudio
import pyttsx3
import speech_recognition as sr
from flask import request, Flask, jsonify

import audioUtils
import client
import serverUtils

global no_voice_mode
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

    threading.Thread(target=client.speak, args=[speech]).start()

    return jsonify("OK")


@app.route("/record", methods=['POST'])
def record_microphone_and_send_back():
    check_api_key()

    record_for_seconds = int(get_body('record_for_seconds'))
    speech_before_input = get_sentence_in_body('speech_before_input')

    client.speak(speech_before_input)

    audioUtils.record(record_for_seconds)

    return serverUtils.send_file_to_server(audioUtils.filename)


def listen():
    if no_voice_mode:
        recognize_main()  # starts listening for your sentence
    else:
        try:
            porcupine = pvporcupine.create(keywords=['jarvis'])
            pa = pyaudio.PyAudio()

            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length
            )

            while True:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                keyword_index = porcupine.process(pcm)

                if keyword_index >= 0:
                    recognize_main()  # starts listening for your sentence

        except Exception as e:
            print("Oops! Une erreur est survenue/je n'ai pas compris")
            print(e)


def start_listening_for_hotword():  # initial keyword call
    print("Waiting for a keyword...")  # Prints to screen
    listen()
    time.sleep(1000000)  # keeps loop running


def recognize_main():  # Main reply call function
    r = sr.Recognizer()

    try:
        if no_voice_mode:
            data = input("Entrez phrase : ").lower()
        else:
            with sr.Microphone(device_index=0) as source:
                r.adjust_for_ambient_noise(source=source, duration=0.5)
                speak(serverUtils.get_random_sentence_with_id('yesSir'))
                audio = r.listen(source, timeout=3, phrase_time_limit=(5 if not no_voice_mode else 1))

            # now uses Google speech recognition
            data = r.recognize_google(audio, language="fr-FR")
            data = data.lower()  # makes all voice entries show as lower case

        print("DATA : " + data)
        speak(serverUtils.send_to_server(data))

    except sr.UnknownValueError:
        speak(serverUtils.get_random_sentence_with_id('dontUnderstand'))
    except sr.RequestError as e:  # if you get a request error from Google speech engine
        print(
            "Erreur du service Google Speech Recognition ; {0}".format(e))
    listen()


def speak(text):
    print(text)
    rate = 100  # Sets the default rate of speech
    engine = pyttsx3.init()  # Initialises the speech engine
    voices = engine.getProperty('voices')  # sets the properties for speech
    engine.setProperty('voice', voices[0])  # Gender and type of voice
    engine.setProperty('rate', rate + 50)  # Adjusts the rate of speech
    engine.say(text)  # tells Python to speak variable 'text'
    engine.runAndWait()  # waits for speech to finish and then continues with program


def startListening():
    hotword = serverUtils.get_hotword()
    print("Getting hotword from server : " + hotword)

    global no_voice_mode
    no_voice_mode = False
    if 'no-voice' in sys.argv:
        print("[WARN] No voice mode enabled")
        no_voice_mode = True

    while 1:  # This starts a loop so the speech recognition is always listening to you
        start_listening_for_hotword()


if __name__ == '__main__':
    thread = threading.Thread(target=startListening)
    thread.start()
    app.run(port=5001, debug=False, host='0.0.0.0', threaded=True)
