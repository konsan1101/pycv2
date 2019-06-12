#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://github.com/respeaker/respeaker_python_library/blob/master/respeaker/bing_speech_api.py

import sys
import os
import time
import codecs
import subprocess

import pyaudio
import speech_recognition as sr
import wave
#import contextlib
#with contextlib.redirect_stdout(None):
#    import pygame.mixer

import json
import requests
import uuid
import http.client
import xml.etree.ElementTree

# Azure
AZURE_SPEECH_KEY = 'xx'

class BingSpeechAPI:
    global AZURE_SPEECH_KEY
    def __init__(self):
        self.key = AZURE_SPEECH_KEY
        self.access_token = None
        self.expire_time = None
        self.locales = {
            'ar-eg': {'Female': 'Microsoft Server Speech Text to Speech Voice (ar-EG, Hoda)'},
            'de-DE': {'Female': 'Microsoft Server Speech Text to Speech Voice (de-DE, Hedda)',
                      'Male': 'Microsoft Server Speech Text to Speech Voice (de-DE, Stefan, Apollo)'},
            'en-AU': {'Female': 'Microsoft Server Speech Text to Speech Voice (en-AU, Catherine)'},
            'en-CA': {'Female': 'Microsoft Server Speech Text to Speech Voice (en-CA, Linda)'},
            'en-GB': {'Female': 'Microsoft Server Speech Text to Speech Voice (en-GB, Susan, Apollo)',
                      'Male': 'Microsoft Server Speech Text to Speech Voice (en-GB, George, Apollo)'},
            'en-IN': {'Male': 'Microsoft Server Speech Text to Speech Voice (en-IN, Ravi, Apollo)'},
            'en-US': {'Female': 'Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)',
                      'Male': 'Microsoft Server Speech Text to Speech Voice (en-US, BenjaminRUS)'},
            'es-ES': {'Female': 'Microsoft Server Speech Text to Speech Voice (es-ES, Laura, Apollo)',
                      'Male': 'Microsoft Server Speech Text to Speech Voice (es-ES, Pablo, Apollo)'},
            'es-MX': {'Male': 'Microsoft Server Speech Text to Speech Voice (es-MX, Raul, Apollo)'},
            'fr-CA': {'Female': 'Microsoft Server Speech Text to Speech Voice (fr-CA, Caroline)'},
            'fr-FR': {'Female': 'Microsoft Server Speech Text to Speech Voice (fr-FR, Julie, Apollo)',
                      'Male': 'Microsoft Server Speech Text to Speech Voice (fr-FR, Paul, Apollo)'},
            'it-IT': {'Male': 'Microsoft Server Speech Text to Speech Voice (it-IT, Cosimo, Apollo)'},
            'ja-JP': {'Female': 'Microsoft Server Speech Text to Speech Voice (ja-JP, Ayumi, Apollo)',
                      'Femal2': 'Microsoft Server Speech Text to Speech Voice (ja-JP, HarukaRUS)',
                      'Male': 'Microsoft Server Speech Text to Speech Voice (ja-JP, Ichiro, Apollo)'},
            'pt-BR': {'Male': 'Microsoft Server Speech Text to Speech Voice (pt-BR, Daniel, Apollo)'},
            'ru-RU': {'Female': 'Microsoft Server Speech Text to Speech Voice (pt-BR, Daniel, Apollo)',
                      'Male': 'Microsoft Server Speech Text to Speech Voice (ru-RU, Pavel, Apollo)'},
            'zh-CN': {'Female': 'Microsoft Server Speech Text to Speech Voice (zh-CN, HuihuiRUS)',
                      'Female2': 'Microsoft Server Speech Text to Speech Voice (zh-CN, Yaoyao, Apollo)',
                      'Male': 'Microsoft Server Speech Text to Speech Voice (zh-CN, Kangkang, Apollo)'},
            'zh-HK': {'Female': 'Microsoft Server Speech Text to Speech Voice (zh-HK, Tracy, Apollo)',
                      'Male': 'Microsoft Server Speech Text to Speech Voice (zh-HK, Danny, Apollo)'},
            'zh-TW': {'Female': 'Microsoft Server Speech Text to Speech Voice (zh-TW, Yating, Apollo)',
                      'Male': 'Microsoft Server Speech Text to Speech Voice (zh-TW, Zhiwei, Apollo)'}
        }

    def authenticate(self):
        accessTokenHost = 'api.cognitive.microsoft.com'
        path = '/sts/v1.0/issueToken'
        params  = ''
        headers = {'Ocp-Apim-Subscription-Key': self.key}

        # Connect to server
        #print ('Connect to server')
        conn = http.client.HTTPSConnection(accessTokenHost)
        conn.request('POST', path, params, headers)
        response = conn.getresponse()
        #print('Response', response.status, response.reason)
        data = response.read()
        #print(data)
        conn.close()

        self.access_token = data.decode('UTF-8')
        #print ("Access Token: " + self.access_token)

    def synthesize(self, text, language='ja-JP', gender='Female'):
        self.authenticate()

        if language not in self.locales.keys():
            raise ValueError('language is not supported.')
        lang = self.locales.get(language)
        if len(lang) == 1:
            gender       = lang.keys()[0]
            #service_name = lang.keys()[0][0]
        service_name = lang[gender]
        if gender in ['Female','Femal2']:
            gender = 'Female'

        synthesizeHost = 'westus.tts.speech.microsoft.com'
        path = '/cognitiveservices/v1'

        body = xml.etree.ElementTree.Element('speak', version='1.0')
        body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice = xml.etree.ElementTree.SubElement(body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', language)
        voice.set('{http://www.w3.org/XML/1998/namespace}gender', gender)
        voice.set('name', service_name)
        voice.text = text

        headers = {"Content-type": "application/ssml+xml", 
			"X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
			"Authorization": "Bearer " + self.access_token, 
			"X-Search-AppId": "xx", 
			"X-Search-ClientID": "xx", 
			"User-Agent": "TTSForPython"}

        # Connect to server
        #print ('Connect to server')
        conn = http.client.HTTPSConnection(synthesizeHost)
        conn.request('POST', path, xml.etree.ElementTree.tostring(body), headers)
        response = conn.getresponse()
        #print('Response', response.status, response.reason)
        data = response.read()
        #print(data)
        conn.close()

        #print("The synthesized wave length: %d" %(len(data)))
        return data

    def recognize(self, audio_data, language='ja-JP'):
        self.authenticate()

        recognizeUrl = 'https://speech.platform.bing.com/recognize/query'
        params = {
            'version': '3.0',
            'requestid': uuid.uuid4(),
            'appID': 'xx',
            'format': 'json',
            'locale': language,
            'device.os': 'wp7',
            'scenarios': 'ulm',
            'instanceid': uuid.uuid4(),
        }
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'audio/wav; samplerate=16000',
        }

        # Request to server
        response = requests.post(recognizeUrl, params=params, headers=headers, data=audio_data)
        #print('Response', response.status_code)
        result = response.json()

        if 'header' not in result or 'lexical' not in result['header']:
            raise ValueError('Unexpected response: {}'.format(result))
        return result['header']['lexical']



def qPlay(tempFile=None, sync=True):

        if not tempFile is None:
            #if os.name != 'nt':
            #    pygame.mixer.init()
            #    pygame.mixer.music.load(tempFile)
            #    pygame.mixer.music.play()
            #    if sync == True:
            #        while pygame.mixer.music.get_busy():
            #            time.sleep(0.1)
            #        pygame.mixer.music.stop()
            #else:
            if tempFile == '_ready':
                tempFile = '_sound_ready.mp3'
            if tempFile == '_accept':
                tempFile = '_sound_accept.mp3'
            if tempFile == '_ok':
                tempFile = '_sound_ok.mp3'
            if tempFile == '_ng':
                tempFile = '_sound_ng.mp3'
            if tempFile == '_shutter':
                tempFile = '_sound_shutter.mp3'
            if os.path.exists(tempFile):
                cmd =  ['sox', tempFile, '-d', '-q']
                #cmd = ['sox', '-v', '3', tempFile, '-d', '-q', 'gain', '-n']
                #cmd = ['sox', '-v', '3', tempFile, '-b', '8', '-u', '-r', '8000', '-c', '1', '-d', '-q', 'gain', '-n']
                #cmd = ['sox', '-v', '3', tempFile, '-r', '8000', '-c', '1', '-d', '-q', 'gain', '-n']
                p=subprocess.Popen(cmd)
                if sync == True:
                    p.wait()



if __name__ == '__main__':
    micdev  = 0
    inplng  = 'ja-JP'
    recText = 'temp/temp_recText.txt'
    recWave = 'temp/temp_recWave.wav'
    if len(sys.argv)>=2:
        micdev  = sys.argv[1]
    if len(sys.argv)>=3:
        inplng  = sys.argv[2]
    if len(sys.argv)>=4:
        recText = sys.argv[3]
    if len(sys.argv)>=5:
        recWave = sys.argv[4]
    if inplng=='ja':
        inplng = 'ja-JP'

    #pa = pyaudio.PyAudio()
    #for i in range(0, pa.get_host_api_count()):
    #    print(i, pa.get_host_api_info_by_index(i))

    print('')
    print('speech_input_azure.py')
    print(' 1)language = ' + inplng)
    print(' 2)recText  = ' + recText)
    print(' 3)recWave  = ' + recWave)

    srr = sr.Recognizer()
    with sr.Microphone(int(micdev)) as source:
        srr.dynamic_energy_threshold = True
        srr.adjust_for_ambient_noise(source, duration=5)
        qPlay('_ready')

        datasize=0
        while datasize<50000 or datasize>300000:
            print(' listning...(' + inplng + ')')
            try:
                speech = srr.listen(source, timeout=15, phrase_time_limit=15)
                data    =speech.get_wav_data(16000,2)
                datasize=sys.getsizeof(data)
            except:
                srr.dynamic_energy_threshold = True
                srr.adjust_for_ambient_noise(source, duration=5)
                datasize=0
            if datasize<50000 or datasize>300000:
                qPlay('_ng')

        print(' accept', datasize, 'byte')
        qPlay('_accept')

        wb = open(recWave, 'wb')
        wb.write(data)
        wb.close
        wb = None

        rb = wave.open(recWave, 'rb')
        audio = rb.readframes(-1)
        rb.close()
        rb = None

        if os.path.exists(recText):
            os.remove(recText)

        txt=''
        try:
            #bing = BingSpeechAPI()
            #txt = bing.recognize(audio, language=inplng)
            txt = srr.recognize_bing(speech, key='xx', language=inplng)

            print(' ' + txt)

            w = codecs.open(recText, 'w', 'shift_jis')
            w.write(txt)
            w.close()
            w = None

        except:
            print(' Error!', sys.exc_info()[0])
            print(txt)
            sys.exit()



