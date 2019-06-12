#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://github.com/respeaker/respeaker_python_library/blob/master/respeaker/bing_speech_api.py
#https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/Samples-Http/Python/TTSSample.py

import sys
import os
import time
import codecs
import subprocess

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

        synthesizeHost = 'speech.platform.bing.com'
        path = '/synthesize'

        body = xml.etree.ElementTree.Element('speak', version='1.0')
        body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice = xml.etree.ElementTree.SubElement(body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', language)
        voice.set('{http://www.w3.org/XML/1998/namespace}gender', gender)
        voice.set('name', service_name)
        voice.text = text

        headers = {"Content-type": "application/ssml+xml", 
			"X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
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
            cmd =  ['sox', tempFile, '-d', '-q']
            #cmd = ['sox', '-v', '3', tempFile, '-d', '-q', 'gain', '-n']
            #cmd = ['sox', '-v', '3', tempFile, '-b', '8', '-u', '-r', '8000', '-c', '1', '-d', '-q', 'gain', '-n']
            #cmd = ['sox', '-v', '3', tempFile, '-r', '8000', '-c', '1', '-d', '-q', 'gain', '-n']
            p=subprocess.Popen(cmd)
            if sync == True:
                p.wait()



if __name__ == '__main__':
    lng     = 'ja-JP'
    txtFile = 'temp/temp_msg.txt'
    tmpFile = 'temp/temp_voice.wav' #Azure, HOYA
    #tmpFile = 'temp/temp_voice.mp3' #Google, Watson
    if len(sys.argv)>=2:
        lng = sys.argv[1]
    if len(sys.argv)>=3:
        txtFile = sys.argv[2]
    if len(sys.argv)>=4:
        tmpFile = sys.argv[3]
    if lng=='ja':
        lng = 'ja-JP'

    print('')
    print('speech_output_azure.py')
    print(' 1)language = ' + lng)
    print(' 2)txtFile  = ' + txtFile)
    print(' 3)tmpFile  = ' + tmpFile)

    txt = ''
    rt = codecs.open(txtFile, 'r', 'shift_jis')
    for t in rt:
        txt = (txt + ' ' + str(t)).strip()
    rt.close
    rt = None

    if os.path.exists(tmpFile):
        os.remove(tmpFile)

    try:
        print(' ' + txt)

        bing = BingSpeechAPI()
        if lng=='ja-JP':
            speech = bing.synthesize(txt, language=lng, gender='Femal2')
        else:
            speech = bing.synthesize(txt, language=lng, gender='Female')

        wb = open(tmpFile, 'wb')
        wb.write(speech)
        wb.close()
        wb = None

    except:
        print(' Error!', sys.exc_info()[0])
        sys.exit()

    if os.path.exists(tmpFile):
        qPlay(tmpFile)



    #text = bing.recognize(speech, language=lng)
    #print(text)



