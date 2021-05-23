import json
import os
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
from playsound import playsound

import audioUtils
import serverUtils

global no_voice_mode
app = Flask(__name__)
token = os.getenv('JARVIS_API_KEY')
path = os.getcwd()


def check_api_key():
    """
    Check the api key in the request and in the environnement variables
    :return: true if the key is valid
    """
    token_given = request.headers.get('Authorization')
    if token_given != token:
        flask.abort(401)


def get_body(name):
    """
    Returns something that's inside the body
    :param name: body arg name
    :return:
    """
    data = json.loads(request.data.decode('utf8'))
    if not isinstance(data, dict):
        data = json.loads(data)

    data = str(data[name])
    return data


def get_sentence_in_body(name):
    """
    Returns the sentence in the body of a request
    :param name: body arg name
    :return: sentence in body
    """
    data = json.loads(str(request.data.decode('utf8')).replace('"', '\"').replace("\'", "'"))
    if not isinstance(data, dict):
        data = json.loads(data)

    data = str(data[name]).lower()
    return data


@app.route("/input", methods=['POST'])
def input_sentence():
    """
    Listen for a given amount of seconds then return the recognized output with google stt.
    :header listen_for_seconds: the amount of seconds you want to record
    :header speech_before_input: what to say before recording input
    """
    check_api_key()

    listen_for_seconds = int(get_body('listen_for_seconds'))
    speech_before_input = get_sentence_in_body('speech_before_input')
    return serverUtils.input_sentence(listen_for_seconds, speech_before_input)


@app.route("/speak", methods=['POST'])
def speak():
    """
    Speak a given text

    :header speech: is the text you want to speak
    :return:
    """
    check_api_key()

    speech = get_body('speech')

    threading.Thread(target=speak_text, args=[speech]).start()

    return jsonify("OK")


@app.route("/sound", methods=['POST'])
def sound():
    """
    Play a sound

    :header sound_name: is the filename with the extension (must be inside the sounds folder)
    """
    check_api_key()

    sound_name = get_body('sound_name')

    threading.Thread(target=playsound("sounds/" + sound_name)).start()

    return jsonify("OK")


@app.route("/record", methods=['POST'])
def record_microphone_and_send_back():
    """
    Record the microphone for a given amount
    of seconds and return the recorded .wav file
    """
    check_api_key()

    record_for_seconds = int(get_body('record_for_seconds'))
    speech_before_input = get_sentence_in_body('speech_before_input')

    speak_text(speech_before_input)

    audioUtils.record(record_for_seconds)

    return serverUtils.send_file_to_server(audioUtils.filename)


def recognize_hotword():
    """
    Listen to the microphone with porcupine and wait
    for the hotword, then proceed to the Google sentence
    recognition
    """
    if no_voice_mode:
        recognize_sentence()  # starts listening for your sentence
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
                    recognize_sentence()  # starts listening for your sentence

        except Exception as e:
            print("Oups! Une erreur est survenue/je n'ai pas compris")
            print(e)


def start_listening_for_hotword():
    """
     Initiates hotword recognition
    """

    print("Détection du mot 'Jarvis' en cours...")  # Prints to screen
    recognize_hotword()
    time.sleep(1000000)  # keeps loop running


def recognize_sentence():
    """
    Use Google STT to convert speech to text after the hotword has been detected
    """
    r = sr.Recognizer()

    try:
        if no_voice_mode:
            data = input("Entrez phrase : ")
        else:
            with sr.Microphone(device_index=0) as source:
                r.adjust_for_ambient_noise(source=source, duration=0.5)
                playsound(path + "\\sounds\\" + "listening.mp3")
                audio = r.listen(source, timeout=3, phrase_time_limit=(5 if not no_voice_mode else 1))

            # now uses Google speech recognition
            data = r.recognize_google(audio, language="fr-FR")

        threading.Thread(target=playsound(path + "\\sounds\\" + "listened.mp3")).start()

        print("Vous : " + data)
        speak_text(serverUtils.send_to_server(data))

    except sr.UnknownValueError:
        speak_text(serverUtils.get_random_sentence_with_id('dont_understand'))
    except sr.RequestError as e:  # if you get a request error from Google speech engine
        print(
            "Erreur du service Google Speech Recognition ; {0}".format(e))

    recognize_hotword()


def speak_text(text):
    """
    Speak text using TTS
    :param text: the text to speak
    """
    print("Jarvis : " + text)
    rate = 100  # Sets the default rate of speech
    engine = pyttsx3.init()  # Initialises the speech engine
    voices = engine.getProperty('voices')  # sets the properties for speech
    engine.setProperty('voice', voices[0])  # Gender and type of voice
    engine.setProperty('rate', rate + 50)  # Adjusts the rate of speech
    engine.say(text)  # tells Python to speak variable 'text'
    engine.runAndWait()  # waits for speech to finish and then continues with program


def start_listening():
    """
    Call the hotword recognition method and set (or not) the no-voice mode
    """
    global no_voice_mode
    no_voice_mode = False
    if 'no-voice' in sys.argv:
        print("[WARN] No voice mode enabled")
        no_voice_mode = True

    while 1:
        start_listening_for_hotword()


# Starts the whole client
if __name__ == '__main__':
    thread = threading.Thread(target=start_listening)
    thread.start()
    app.run(port=5001, debug=False, host='0.0.0.0', threaded=True)
