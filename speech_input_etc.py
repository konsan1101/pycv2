#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
#lng = 'en-US'
lng  = 'ja-JP'

print('')
print('※Google Cloudは設定が必要です')

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print('')
    print(' Listning...(' + lng + ')')
    #r = sr.Recognizer()
    r.adjust_for_ambient_noise(source, duration=1)
    r.dynamic_energy_threshold = True
    speech = r.listen(source)
    print(' Accept...')

print('')

# recognize speech using Microsoft Bing Voice Recognition
BING_KEY = 'xx'  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
print('<Microsoft Bing>')
try:
    result = r.recognize_bing(speech, key=BING_KEY, language=lng)
    print('Microsoft Bing : ' + result)
except sr.UnknownValueError:
    print('Microsoft Bing Voice Recognition could not understand audio')
except sr.RequestError as e:
    print('Could not request results from Microsoft Bing Voice Recognition service; {0}'.format(e))



# recognize speech using Google Speech Recognition
print('<Google Speech>')
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key='GOOGLE_SPEECH_RECOGNITION_API_KEY')`
    # instead of `r.recognize_google(audio)`
    result = r.recognize_google(speech, language=lng)
    result = str(result).strip()
    print('Google Speech  : ' + result)
except sr.UnknownValueError:
    print('Google Speech Recognition could not understand audio')
except sr.RequestError as e:
    print('Could not request results from Google Speech Recognition service; {0}'.format(e))



# recognize speech using Google Cloud Speech

#GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""C:\pycv\SpeechRrecognition_test_gcloud.json"""

GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""
{
}
"""

print('<Google Cloud>')
try:
    result = r.recognize_google_cloud(speech,credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS,language=lng)
    result = str(result).strip()
    print('Google Cloud   : ' + result)
except sr.UnknownValueError:
    print('Google Cloud Speech could not understand audio')
except sr.RequestError as e:
    print('Could not request results from Google Cloud Speech service; {0}'.format(e))



