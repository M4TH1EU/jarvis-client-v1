import struct
import sys
import time

import pvporcupine
import pyaudio
import pyttsx3
import speech_recognition as sr

import serverUtils

no_voice_mode = False


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
                    speak(serverUtils.get_random_sentence_with_id('yesSir'))
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
                audio = r.listen(source, timeout=3, phrase_time_limit=(7 if not no_voice_mode else 1))

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


if __name__ == '__main__':
    hotword = serverUtils.get_hotword()
    print("Getting hotword from server : " + hotword)

    while 1:  # This starts a loop so the speech recognition is always listening to you
        if 'no-voice' in sys.argv:
            print("[WARN] No voice mode enabled")
            no_voice_mode = True

        start_listening_for_hotword()
