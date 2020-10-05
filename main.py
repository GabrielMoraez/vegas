#!/usr/bin/env python3

import sys
sys.path.insert(0, '/scripts')
import time
import pygame
import random
import speech_recognition as sr

from scripts.watson import *

from scripts.weather import *

text_talker = TextTalker()
weather = Weather()

list = ["water", "fire", "earth"]
greetings = ["Hello, how can I help you?", "Yes?", "Hello", "What can I do for you?"]

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
  recognizer = sr.Recognizer()
  microphone = sr.Microphone()
  n = random.randint(0,3)

  instructions = (
    greetings[n]
  )

  text_talker.say(instructions)
  # show instructions and wait 3 seconds before starting the game

  print('Say something')
  action = recognize_speech_from_mic(recognizer, microphone)
  print("You said: {}".format(action["transcription"]))

  if 'weather' in format(action["transcription"]):
    response = weather.getWeather('Rio de Janeiro, BR')
    print(response)
    response_text = f"Looks like we have {response} today"
    text_talker.say(response_text)
  elif 'temperature' in format(action["transcription"]):
    response = weather.getCurrentTemperature('Rio de Janeiro, BR')
    response_text = f"Current temperature of {response['temp']} Celsius in Rio de Janeiro"
    text_talker.say(response_text)
  else:
    text_talker.say("I can't help you yet")