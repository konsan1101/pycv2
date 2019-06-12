#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import queue
import threading
import subprocess
import datetime
import time
import codecs

import pyaudio
import speech_recognition as sr
import wave
#import contextlib
#with contextlib.redirect_stdout(None):
#    import pygame.mixer
import ctypes

import json
import requests
import uuid
import http.client
import xml.etree.ElementTree

from googletrans import Translator
#import goslate
from gtts import gTTS
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud import LanguageTranslatorV3
from watson_developer_cloud import TextToSpeechV1

print(os.path.dirname(__file__))
print(os.path.basename(__file__))
print(sys.version_info)



qLogNow=datetime.datetime.now()
qLogFlie = 'temp/log/' + qLogNow.strftime('%Y%m%d-%H%M%S') + '_' + os.path.basename(__file__) + '.log'
def qLogOutput(logText='', display=True, outfile=True):
    if display == True:
        print(str(logText))
    if outfile == True:
        w = codecs.open(qLogFlie, 'a', 'utf-8')
        w.write(str(logText) + '\n')
        w.close()
        w = None

qLogOutput(qLogFlie,True,True)



srr  = sr.Recognizer()
srr2 = sr.Recognizer()

# Azure
AZURE_SPEECH_KEY = 'xx'

# win32
import win32com.client as wincl
import win32api

# Google Cloud
google_translator = Translator()
#google_translator = goslate.Goslate(service_urls=['https://translate.google.com'])
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""
{
}
"""

# Watson
watson_STT = None
watson_TTS = None
watson_translator = None
try:
    watson_STT = SpeechToTextV1(
            url='https://stream.watsonplatform.net/speech-to-text/api',
            username='xx',
            password='XX')
    watson_translator = LanguageTranslatorV3(
            version='2018-05-01',
            url='https://gateway.watsonplatform.net/language-translator/api',
            username='xx',
            password='XX')
    watson_TTS = TextToSpeechV1(
            url='https://stream.watsonplatform.net/text-to-speech/api',
            username='xx',
            password='xx')
except:
    watson_STT = None
    watson_TTS = None
    watson_translator = None

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

        #SSML prosody Element exsample
        #https://www.w3.org/TR/2009/REC-speech-synthesis-20090303/#edef_prosody
        #<prosody pitch='x-low', 'low', 'medium', 'high', 'x-high', or 'default'>
        #<prosody range='x-low', 'low', 'medium', 'high', 'x-high', or 'default'>
        #<prosody rate='+10%', 'x-slow', 'slow', 'medium', 'fast', 'x-fast', or 'default'>
        #<prosody volume='0.0'-'100.0', 'silent', 'x-soft', 'soft', 'medium', 'loud', 'x-loud', or 'default'>

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
        #qLogOutput('Response, ' + response + ', ' + status_code)
        result = response.json()

        if 'header' not in result or 'lexical' not in result['header']:
            raise ValueError('Unexpected response: {}'.format(result))
        return result['header']['lexical']



def qVoiceInput(useApi, inpLang='ja', waveFile=None, outputQ=None, ):
    result=''

    api=useApi
    lng=''
    mdl=''
    if api=='watson' or api=='azure':
        if inpLang=='ar':
            lng='ar-AR'
            mdl='ar-AR_BroadbandModel'
        if inpLang=='en' or inpLang=='en-US':
            lng='en-US'
            mdl='en-US_BroadbandModel'
        if inpLang=='es':
            lng='es-ES'
            mdl='es-ES_BroadbandModel'
        if inpLang=='de':
            lng='de-DE'
            mdl='de-DE_BroadbandModel'
        if inpLang=='fr':
            lng='fr-FR'
            mdl='fr-FR_BroadbandModel'
        if inpLang=='it':
            lng='it-IT'
            mdl='it-IT_BroadbandModel'
        if inpLang=='ja' or inpLang=='ja-JP':
            lng='ja-JP'
            mdl='ja-JP_BroadbandModel'
        if inpLang=='pt':
            lng='pt-BR'
            mdl='pt-BR_BroadbandModel'
        if inpLang=='zh' or inpLang=='zh-CN':
            lng='zh-CN'
            mdl='zh-CN_BroadbandModel'
        if lng == '':
            api='free'

    if api=='watson':
        res   =''
        try:
            rb=open(waveFile, 'rb')
            res = watson_STT.recognize(audio=rb, content_type='audio/wav', model=mdl,
               timestamps=True, word_confidence=True).get_result()
            rb.close()
            rb=None

            result = res['results'][0]['alternatives'][0]['transcript']
            if inpLang=='ja' or inpLang=='ja-JP':
                 result = str(result).replace(' ', '')
            result = str(result).strip()
        except:
            qLogOutput(res)
        if result == '':
            api='free'

    if api=='azure':
        rs = wave.open(waveFile, 'rb')
        rawdata = rs.readframes(rs.getnframes())
        rs.close()
        rs = None
        #with sr.AudioFile(waveFile) as source:
        #    audio = srr2.record(source)

        try:
            bing = BingSpeechAPI()
            result = bing.recognize(rawdata, language=lng)
            #result = srr2.recognize_bing(audio, key='d3c0cb2b3617405c96041af5bc890b79', language=lng)
            if result.lower() == 'x':
                result = ''
        except:
            pass
        if result == '':
            api='free'

    if api=='google' or api=='free':
        with sr.AudioFile(waveFile) as source:
            audio = srr2.record(source)

        try:
            if api=='free':
                result=srr2.recognize_google(audio, language=inpLang)
            else:
                result = srr2.recognize_google_cloud(audio,
                    credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS,
                    language=inpLang)
            result = str(result).strip()
        except:
            pass

        if result != '':
            if useApi != 'google' and useApi != 'free':
                result = '!Google, ' + result

    return result



def qTranslator(useApi, inpLang='ja', outLang='en', transText=u'こんにちわ', outputQ=None, ):
    result=''

    if transText[0:9] != '!Google, ':
        trntxt=transText
    else:
        trntxt=transText[9:]

    api=useApi
    inp=''
    out=''
    if inpLang == outLang:
        api = 'none'

    if api=='watson' or api=='azure':
        if inpLang=='ar':
            inp='ar-AR'
        if inpLang=='en' or inpLang=='en-US':
            inp='en-US'
        if inpLang=='es':
            inp='es-ES'
        if inpLang=='de':
            inp='de-DE'
        if inpLang=='fr':
            inp='fr-FR'
        if inpLang=='it':
            inp='it-IT'
        if inpLang=='ja' or inpLang=='ja-JP':
            inp='ja-JP'
        if inpLang=='pt':
            inp='pt-BR'
        if inpLang=='zh' or inpLang=='zh-CN':
            inp='zh-CN'

        if outLang=='ar':
            out='ar-AR'
        if outLang=='en' or outLang=='en-US':
            out='en-US'
        if outLang=='es':
            out='es-US'
        if outLang=='de':
            out='de-DE'
        if outLang=='fr':
            out='fr-FR'
        if outLang=='it':
            out='it-IT'
        if outLang=='ja' or outLang=='ja-JP':
            out='ja-JP'
        if outLang=='pt':
            out='pt-BR'
        if outLang=='zh' or outLang=='zh-CN':
            out='zh-CN'

        if inp == '' or out == '':
            api='free'

    t=trntxt.replace(' ','_')
    t=t.replace(u'　','_')
    t=t.replace('"','_')
    t=t.replace('$','_')
    t=t.replace('%','_')
    t=t.replace('&','_')
    t=t.replace("'",'_')
    t=t.replace('\\','_')
    t=t.replace('|','_')
    t=t.replace('*','_')
    t=t.replace('/','_')
    t=t.replace('?','_')
    t=t.replace(':',',')
    t=t.replace('<','_')
    t=t.replace('>','_')

    cacheFile='temp/cache/' + t + '_' + inpLang + '_' + outLang + '_' + api + '_utf8.txt'

    apirun = True
    if api != 'none':
        if os.path.exists(cacheFile):
            try:
                txt = ''
                rt = codecs.open(cacheFile, 'r', 'utf-8')
                for t in rt:
                    txt = (txt + ' ' + str(t)).strip()
                rt.close
                rt = None

                result=txt
                if reslut != '':
                    apirun = False
            except:
                rt = None

    if apirun == True:

        if api == 'none':
           result = trntxt

        if api=='watson':
            res  = ''
            res1 = ''
            res2 = ''
            try:
                if inp=='en-US' or out=='en-US':
                    res = watson_translator.translate(text=trntxt, source=inp, target=out).get_result()
                    try:
                        result = res['translations'][0]['translation']
                        result = str(result).strip()
                    except:
                        qLogOutput(res)
                else:
                    res1 = watson_translator.translate(text=trntxt, source=inp, target='en-US').get_result()
                    try:
                        result1 = res1['translations'][0]['translation']
                        result1 = str(result1).strip()
                        res2 = watson_translator.translate(text=res1, source='en-US', target=out).get_result()
                        try:
                            result2 = res2['translations'][0]['translation']
                            result2 = str(result2).strip()
                            result  = result2
                        except:
                            qLogOutput(res2)
                    except:
                        qLogOutput(res1)
            except:
                pass
            if result == '':
                api='free'

        if api=='azure':
            res  = ''
            try:
                token = requests.post('https://api.cognitive.microsoft.com/sts/v1.0/issueToken',
                    headers = {'Content-Type': 'application/json',
                               'Ocp-Apim-Subscription-Key': 'xx',})
                res = requests.get('https://api.microsofttranslator.com/v2/http.svc/Translate',
                    headers = {'Content-Type': 'application/xml',},
                    params={'appid': 'Bearer ' + token.text,
                            'text': trntxt,
                            'from': inp,
                            'to': out,
                            'category': 'general',})
                resxml = res.text
                result = xml.etree.ElementTree.fromstring(resxml).text
            except:
                pass
            if result == '':
                api='free'
            else:
                if result.lower() == 'x':
                    result = ''

        if api=='google' or api=='free':
            res = ''

            # googletrans
            txtary = google_translator.translate([trntxt], src=inpLang, dest=outLang)
            # goslate
            #txtary = google_translator.translate([trntxt], outLang, inpLang)
            for t in txtary:
                res += t.text
            res = str(res).strip()
            if res != '':
                result=res
                if useApi != 'google' and useApi != 'free':
                    result= '!Google, ' + res

    if apirun == True and result != '':
        if api != 'none':
            try:
                w = codecs.open(cacheFile, 'w', 'utf-8')
                w.write(result)
                w.close()
                w = None
            except:
                w = None

    return result



qVoiceOutput_count=0
def qVoiceOutput(useApi, outLang='en', outText='Hallo', tempFile=None, outq=None, outputQ=None, ):
    global qVoiceOutput_count
    qVoiceOutput_count += 1

    if outText[0:9] != '!Google, ':
        outtxt=outText
    else:
        outtxt=outText[9:]

    api=useApi
    lng  =''
    voice=''
    if api=='watson' or api=='azure' or api=='win32':
        if outLang=='en' or outLang=='en-US':
            lng  ='en-US'
            voice='en-US_AllisonVoice'
        if outLang=='es':
            lng  ='es-US'
            voice='es-US_SofiaVoice'
        if outLang=='de':
            lng  ='de-DE'
            voice='de-DE_BirgitVoice'
        if outLang=='fr':
            lng  ='fr-FR'
            voice='fr-FR_ReneeVoice'
        if outLang=='it':
            lng  ='it-IT'
            voice='it-IT_FrancescaVoice'
        if outLang=='ja' or outLang=='ja-JP':
            lng  ='ja-JP'
            voice='ja-JP_EmiVoice'
        if outLang=='pt':
            lng  ='pt-BR'
            voice='pt-BR_IsabelaVoice'
        if lng == '':
            api='free'

    t=outtxt.replace(' ','_')
    t=t.replace(u'　','_')
    t=t.replace('"','_')
    t=t.replace('$','_')
    t=t.replace('%','_')
    t=t.replace('&','_')
    t=t.replace("'",'_')
    t=t.replace('\\','_')
    t=t.replace('|','_')
    t=t.replace('*','_')
    t=t.replace('/','_')
    t=t.replace('?','_')
    t=t.replace(':',',')
    t=t.replace('<','_')
    t=t.replace('>','_')

    now=datetime.datetime.now()
    #stamp=now.strftime('%S')
    #stamp=now.strftime('%S.%f')
    stamp='{0:02d}'.format(qVoiceOutput_count % 100)
    if (api != 'azure') and (api != 'win32'):
        cacheFile='temp/cache/' + t + '_' + outLang + '_' + api + '.mp3'
        tempFilex='temp/temp_voice_' + stamp + '.mp3'
    else:
        cacheFile='temp/cache/' + t + '_' + outLang + '_' + api + '.wav'
        tempFilex='temp/temp_voice_' + stamp + '.wav'

    if tempFile is None:
        tempFile = tempFilex

    apirun = True
    if os.path.exists(cacheFile):

        try:
            rb = open(cacheFile, 'rb')
            wav=rb.read()
            rb.close
            rb = None

            wb = open(tempFile, 'wb')
            wb.write(wav)
            wb.close
            wb = None

            apirun = False
        except:
            rb = None
            wb = None

    if apirun == True:

        if tempFile is None:
            tempFile=tempFilex

        if api=='watson':
            try:
                audio=watson_TTS.synthesize(text=outtxt, accept='audio/mp3', voice=voice).get_result().content
                wb = open(tempFile, 'wb')
                wb.write(audio)
                wb.close()
                wb = None
            except:
                api='free'

        if api=='azure':
            try:
                bing = BingSpeechAPI()
                if lng=='ja-JP':
                    audio = bing.synthesize(outtxt, language=lng, gender='Femal2')
                    #audio = bing.synthesize(outtxt, language=lng, gender='Female')
                else:
                    if lng != 'it-IT' and lng != 'pt-BR':
                        audio = bing.synthesize(outtxt, language=lng, gender='Female')
                    else:
                        audio = bing.synthesize(outtxt, language=lng, gender='Male')

                wb = open(tempFile, 'wb')
                wb.write(audio)
                wb.close()
                wb = None
            except:
                api='free'

        if api=='win32':
            try:
                engine = wincl.Dispatch('SAPI.SpVoice')
                #engine.Speak(t)

                t  = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
                t += '<voice xml:lang="' + lng + '" gender="female">'
                t += outtxt.encode('shift-jis')
                t += '</voice></speak>'

                stream = wincl.Dispatch("SAPI.SpFileStream")
                stream.open(tmpFile, 3, False)
                engine.AudioOutputStream = stream
                engine.Speak(t)
                stream.close()

            except:
                api='free'

        if api=='google' or api=='free':
            try:
                tts = gTTS(text=outtxt, lang=outLang, slow=False)
                tts.save(tempFile)
                if useApi != 'google' and useApi != 'free':
                    outtxt = '!Google, ' + outtxt
            except:
                pass

    if apirun == True:
        try:
            rb = open(tempFile, 'rb')
            wav=rb.read()
            rb.close
            rb = None

            wb = open(cacheFile, 'wb')
            wb.write(wav)
            wb.close
            wb = None
        except:
            rb = None
            wb = None

    if os.path.exists(tempFile):
        qPlay(tempFile, outputQ=outputQ)

    return outtxt



def qVoiceApiInfo(inpApi=None, trnApi=None, outApi=None, outputQ=None, ):

    if not inpApi is None:
        vtext = 'Speech recognition uses '
        if inpApi == 'free':
            vtext += 'free Google speech API,'
            vhalo  = 'Hello, I am free Google.'
        if inpApi == 'google':
            vtext += 'Google Cloud Platform,'
            vhalo  = 'Hello, I am Google.'
        if inpApi == 'watson':
            vtext += 'IBM Watson Developer Cloud,'
            vhalo  = 'Hello, I am IBM Watson.'
        if inpApi == 'azure':
            vtext += 'Microsoft Azure Cognitive Services,'
            vhalo  = 'Hello, I am Microsoft Azure.'
        vtext += ' Speech to Text function,'

        qVoiceOutput(useApi=inpApi, outLang='en', outText=vhalo, outputQ=outputQ)
        qVoiceOutput(useApi=inpApi, outLang='en', outText=vtext, outputQ=outputQ)

    if not trnApi is None:
        vtext = 'Text Translation uses '
        if trnApi == 'free':
            vtext += 'free Google speech API,'
            vhalo  = 'Hello, I am free Google.'
        if trnApi == 'google':
            vtext += 'Google Cloud Platform,'
            vhalo  = 'Hello, I am Google.'
        if trnApi == 'watson':
            vtext += 'IBM Watson Developer Cloud,'
            vhalo  = 'Hello, I am IBM Watson.'
        if trnApi == 'azure':
            vtext += 'Microsoft Azure Cognitive Services,'
            vhalo  = 'Hello, I am Microsoft Azure.'
        vtext += ' Translation function,'

        if trnApi != inpApi:
            qVoiceOutput(useApi=trnApi, outLang='en', outText=vhalo, outputQ=outputQ)
        qVoiceOutput(useApi=trnApi, outLang='en', outText=vtext, outputQ=outputQ)

    if not outApi is None:
        vtext = 'Text Vocalization uses '
        if outApi == 'free':
            vtext += 'free Google speech API,'
            vhalo  = 'Hello, I am free Google.'
        if outApi == 'google':
            vtext += 'Google Cloud Platform,'
            vhalo  = 'Hello, I am Google.'
        if outApi == 'watson':
            vtext += 'IBM Watson Developer Cloud,'
            vhalo  = 'Hello, I am IBM Watson.'
        if outApi == 'azure':
            vtext += 'Microsoft Azure Cognitive Services,'
            vhalo  = 'Hello, I am Microsoft Azure.'
        vtext += ' Text to Speech function,'

        if outApi != inpApi and outApi != trnApi:
            qVoiceOutput(useApi=outApi, outLang='en', outText=vhalo, outputQ=outputQ)
        qVoiceOutput(useApi=outApi, outLang='en', outText=vtext, outputQ=outputQ)



def qPlay(tempFile=None, outputQ=None, sync=True):
    global inpBusy
    global inpLast
    global playBusy
    global playLast

    if (not tempFile is None) and (not outputQ is None):
        outputQ.put(['file', tempFile])
        outputQ.put(['file', '_!playing'])
    else:

        if not tempFile is None:

            if (outputQ is None) and (sync == True):
                if inpBusy != False:
                    qLogOutput('qPlay___:' + str(inpBusy) + '...wait')
                    chktime = time.time()
                    while (inpBusy != False) and (int(time.time() - chktime) < 5):
                        time.sleep(0.1)
                        inpSec = int(time.time() - inpLast)
                #inpSec  = int(time.time() - inpLast)
                #if inpSec < 1:
                #    chktime = time.time()
                #    while (inpSec < 1)  and (int(time.time() - chktime) < 5):
                #        time.sleep(0.1)
                #        inpSec = int(time.time() - inpLast)

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

                playBusy = 'Playing'
                playLast = time.time()

                cmd =  ['sox', tempFile, '-d', '-q']
                #cmd = ['sox', '-v', '3', tempFile, '-d', '-q', 'gain', '-n']
                #cmd = ['sox', '-v', '3', tempFile, '-b', '8', '-u', '-r', '8000', '-c', '1', '-d', '-q', 'gain', '-n']
                #cmd = ['sox', '-v', '3', tempFile, '-r', '8000', '-c', '1', '-d', '-q', 'gain', '-n']
                p=subprocess.Popen(cmd)
                if sync == True:
                    p.wait()

                playBusy = False
                playLast = time.time()

    playBusy = False



def sub_input_wait(runmode, micdev, mictype, julius_adingui, julius_beatgui, outputQ, outputQ2, playtextQ, playtextQ2,):
    global inpBusy
    global inpLast
    global compBusy
    global compLast
    global textBusy
    global textLast
    global outBusy
    global outLast
    global playBusy
    global playLast

    if mictype != 'usb':
        inpWait  = 0
        compWait = 0
        textWait = 3
        outWait  = 2
        playWait = 2
    else:
        inpWait  = 0
        compWait = 0
        textWait = 3
        outWait  = 2
        playWait = 1

    inpSec  = int(time.time() - inpLast)
    compSec = int(time.time() - compLast)
    textSec = int(time.time() - textLast)
    outSec  = int(time.time() - outLast)
    playSec = int(time.time() - playLast)
    allchktime = time.time()
    while  ((runmode != 'speech') or str(micdev).lower() == 'file') \
       and ((playtextQ.qsize() > 0 or playtextQ2.qsize() > 0) \
        or  (outputQ.qsize() > 0   or outputQ2.qsize() > 0)   \
        or  (compBusy != False and compWait > 0) \
        or  (compSec  < compWait) \
        or  (textBusy != False and textWait > 0) \
        or  (textSec  < textWait) \
        or  (outBusy  != False  and outWait > 0) \
        or  (outSec   < outWait ) \
        or  (playBusy != False and playWait > 0) \
        or  (playSec  < playWait)) \
       and (int(time.time() - allchktime) < 30):

        if not julius_adingui is None and os.name == 'nt':
            if int(time.time() - julius_beatgui) >= 1:
                try:
                    hWnd = ctypes.windll.user32.FindWindowW('SDL_app',None)
                    if hWnd is not 0:
                        ctypes.windll.user32.ShowWindow(hWnd, 2)
                except:
                    pass

        if (playtextQ.qsize() > 0 or playtextQ2.qsize() > 0):
            qLogOutput('input___:playtextQ...wait')
            chktime = time.time()
            while (playtextQ.qsize() > 0 or playtextQ2.qsize() > 0) \
              and (int(time.time() - chktime) < 5):
                time.sleep(0.1)

        if (outputQ.qsize() > 0 or outputQ2.qsize() > 0):
            qLogOutput('input___:outputQ...wait')
            chktime = time.time()
            while (outputQ.qsize() > 0 or outputQ2.qsize() > 0) \
              and (int(time.time() - chktime) < 5):
                time.sleep(0.1)

        compSec = int(time.time() - compLast)
        if (compBusy != False and compWait > 0) or (compSec < compWait):
            qLogOutput('input___:compBusy ' + str(compBusy) + '...wait')
            chktime = time.time()
            while (compBusy != False and compWait > 0) and (int(time.time() - chktime) < 5):
                time.sleep(0.1)
                compSec = int(time.time() - compLast)
            while (compSec < compWait):
                time.sleep(0.1)
                compSec = int(time.time() - compLast)

        textSec = int(time.time() - textLast)
        if (textBusy != False and textWait > 0) or (textSec < textWait):
            qLogOutput('input___:textBusy ' + str(textBusy) + '...wait')
            chktime = time.time()
            while (textBusy != False and textWait > 0) and (int(time.time() - chktime) < 5):
                time.sleep(0.1)
                textSec = int(time.time() - textLast)
            while (textSec < textWait):
                time.sleep(0.1)
                textSec = int(time.time() - textLast)

        outSec = int(time.time() - outLast)
        if (outBusy != False and outWait > 0) or (outSec < outWait):
            qLogOutput('input___:outBusy ' + str(outBusy) + '...wait')
            chktime = time.time()
            while (outBusy != False and outWait > 0) and (int(time.time() - chktime) < 5):
                time.sleep(0.1)
                outSec = int(time.time() - outLast)
            while (outSec < outWait):
                time.sleep(0.1)
                outSec = int(time.time() - outLast)

        playSec = int(time.time() - playLast)
        if (playBusy != False and playWait > 0) or (playLast < playWait):
            qLogOutput('input___:playBusy ' + str(playBusy) + '...wait')
            chktime = time.time()
            while (playBusy != False and playWait > 0) and (int(time.time() - chktime) < 5):
                time.sleep(0.1)
                playSec = int(time.time() - playLast)
            while (playSec < playWait):
                time.sleep(0.1)
                playSec = int(time.time() - playLast)



input_beat=0
julius_adintool = None
julius_adingui  = None
def sub_input(cn_r, cn_s, outputQ, outputQ2, playtextQ, playtextQ2,):
    global input_beat
    global julius_adintool
    global julius_adingui

    global inpApi
    global trnApi
    global outApi
    global inpLang
    global trnLang
    global outLang
    global txtLang
    global micLevel

    global inpBusy
    global inpLast

    qLogOutput('input___:init')

    runmode  = cn_r.get()
    micdev   = cn_r.get()
    mictype  = cn_r.get()
    micguide = cn_r.get()
    micON    = cn_r.get()
    recSJISf = cn_r.get()
    cn_r.task_done()

    qLogOutput('input___:runmode =' + str(runmode ))
    qLogOutput('input___:micdev  =' + str(micdev  ))
    qLogOutput('input___:mictype =' + str(mictype ))
    qLogOutput('input___:micguide=' + str(micguide))
    qLogOutput('input___:micON   =' + str(micON   ))
    qLogOutput('input___:recSJISf=' + str(recSJISf))

    qLogOutput('input___:start')

    listner = 'sr'

    julius_rewind   = '1111'
    julius_headmg   = '444'
    julius_tailmg   = '666'
    julius_count    = 0
    julius_beattool = time.time()
    julius_beatgui  = time.time()
    if int(micLevel) != 0:
        adintool_exe = 'julius/adintool.exe'
        adintool_gui = 'julius/adintool-gui.exe'
        if os.path.exists(adintool_exe):
            if os.path.exists(adintool_gui):
                listner = 'julius'

    onece = True
    while True:
        input_beat = time.time()

        if cn_r.qsize() > 0:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if mode_get is None:
                qLogOutput('input___:None=break')
                break

            if cn_r.qsize() != 0 or cn_s.qsize() > 2:
                qLogOutput('input___: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if mode_get == 'START':
                cn_s.put(['INIT', ''])

            elif mode_get != 'INIT' and mode_get != 'READY' and mode_get != 'NEXT':
                cn_s.put(['PASS', ''])

            elif str(micdev).lower() == 'file':
                if micON != 'None':
                    if not os.path.exists(micON):
                        qLogOutput('input___:Synchronize(' + micON + ')...wait')
                        while not os.path.exists(micON):
                            time.sleep(0.3)
                if recSJISf != 'Default' and micON != 'None':
                    if os.path.exists(recSJISf):
                        qLogOutput('input___:Synchronize(' + recSJISf + ')...wait')
                        while os.path.exists(recSJISf):
                            time.sleep(0.3)

                inpBusy = False
                #####sub_input_wait(runmode, micdev, mictype, julius_adingui, julius_beatgui, outputQ, outputQ2, playtextQ, playtextQ2,)

                micWave='temp/temp_micWave.wav'
                bakWave='temp/temp_bakWave.wav'

                inpBusy = micWave
                inpLast = time.time()

                now=datetime.datetime.now()
                stamp=now.strftime('%Y%m%d-%H%M%S')
                voicef = 'temp/voices/' + stamp + '_voice.wav'

                if os.path.exists(micWave):
                    inpBusy = 'Reading'
                    inpLast = time.time()

                    if os.path.exists(bakWave):
                        os.remove(bakWave)

                    chktime = time.time()
                    while (os.path.exists(micWave)) and (int(time.time() - chktime) < 2):
                        try:
                            os.rename(micWave, bakWave)

                            if runmode != 'number':
                                #sox = subprocess.Popen(['sox', bakWave, '-r', '16000', '-b', '16', '-c', '1', voicef, '-q', \
                                #                        'equalizer', '800', '1.0q', '7', ])
                                sox = subprocess.Popen(['sox', bakWave, '-r', '16000', '-b', '16', '-c', '1', voicef, '-q', ])
                            else:
                                #sox = subprocess.Popen(['sox', bakWave, '-r', '16000', '-b', '16', '-c', '1', voicef, '-q', \
                                #                        'equalizer', '800', '1.0q', '7', 'tempo', '0.9', ])
                                sox = subprocess.Popen(['sox', bakWave, '-r', '16000', '-b', '16', '-c', '1', voicef, '-q', ])
                            sox.wait()
                            sox.terminate()
                            sox = None

                        except:
                            pass
                        time.sleep(0.1)

                if not os.path.exists(voicef):
                    inpBusy = False
                    inpLast = time.time()
                    cn_s.put(['NG', ''])
                    time.sleep(0.5)

                else:
                    #qLogOutput('input___:file=' + micWave + ' to ' + voicef)
                    inpBusy = False
                    inpLast = time.time()
                    cn_s.put(['stamp',  stamp])
                    cn_s.put(['voicef', voicef])
                    time.sleep(0.5)

            else:
                if micON != 'None':
                    if not os.path.exists(micON):
                        qLogOutput('input___:Synchronize(' + micON + ')...wait')
                        while not os.path.exists(micON):
                            time.sleep(0.3)
                if recSJISf != 'Default' and micON != 'None':
                    if os.path.exists(recSJISf):
                        qLogOutput('input___:Synchronize(' + recSJISf + ')...wait')
                        while os.path.exists(recSJISf):
                            time.sleep(0.3)

                if listner == 'julius':
                    for i in range(1,99):
                        julius_file  = 'temp/voices/julius.' + '{0:04d}'.format(i) + '.wav'
                        if os.path.exists(julius_file):
                            try:
                                os.remove(julius_file)
                            except:
                                pass

                    if mictype == 'usb':
                        if julius_adintool is None:
                            while int(time.time() - julius_beatgui) < 2:
                                time.sleep(0.1)
                            julius_adintool = subprocess.Popen([adintool_exe, '-in', 'mic', \
                                              '-rewind', julius_rewind, '-headmargin', julius_headmg, '-tailmargin', julius_tailmg, \
                                              '-lv', str(micLevel), '-zmean', \
                                              '-out', 'file', '-filename', 'temp/voices/julius', '-startid', '1', ], \
                                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                            julius_count    = 0
                            julius_beattool = time.time()

                        if julius_adingui is None:
                            while int(time.time() - julius_beattool) < 2:
                                time.sleep(0.1)
                            #startup = subprocess.STARTUPINFO()
                            #startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                            #startup.wShowWindow = subprocess.SW_HIDE
                            julius_adingui  = subprocess.Popen([adintool_gui, '-in', 'mic', \
                                              '-rewind', julius_rewind, '-headmargin', julius_headmg, '-tailmargin', julius_tailmg, \
                                              '-lv', str(micLevel), '-zmean', ], \
                                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                                              #stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startup)
                            julius_beatgui  = time.time()

                inpBusy = False
                sub_input_wait(runmode, micdev, mictype, julius_adingui, julius_beatgui, outputQ, outputQ2, playtextQ, playtextQ2,)

                if micguide != 'off':
                    qPlay('_ready', outputQ=None)

                inpBusy = 'Listning'
                inpLast = time.time()

                stamp   = ''
                voicef  = ''

                if listner == 'julius':
                    julius_hit_file = ''
                    julius_hit_sec  = 99

                    if julius_adintool is None:
                            while int(time.time() - julius_beatgui) < 2:
                                time.sleep(0.1)
                            julius_adintool = subprocess.Popen([adintool_exe, '-in', 'mic', \
                                              '-rewind', julius_rewind, '-headmargin', julius_headmg, '-tailmargin', julius_tailmg, \
                                              '-lv', str(micLevel), '-zmean', \
                                              '-out', 'file', '-filename', 'temp/voices/julius', '-startid', '1'], \
                                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                            julius_count    = 0
                            julius_beattool = time.time()

                    julius_count += 1
                    julius_file  = 'temp/voices/julius.' + '{0:04d}'.format(julius_count  ) + '.wav'
                    julius_file1 = 'temp/voices/julius.' + '{0:04d}'.format(julius_count+1) + '.wav'
                    julius_file2 = 'temp/voices/julius.' + '{0:04d}'.format(julius_count+2) + '.wav'
                    while os.path.exists(julius_file):
                        try:
                            os.remove(julius_file)
                            julius_count += 1
                            julius_file  = 'temp/voices/julius.' + '{0:04d}'.format(julius_count) + '.wav'
                        except:
                            break

                    qLogOutput('input___:☆Waitting[lv=' + str(micLevel) + ']...(' + julius_file + ')')
                    wait_start=time.time()

                    julius_sec = int(time.time() - wait_start)
                    #while julius_sec <= 10:
                    while julius_sec <= 5:

                        if julius_adingui is None:
                            while int(time.time() - julius_beattool) < 2:
                                time.sleep(0.1)
                            #startup = subprocess.STARTUPINFO()
                            #startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                            #startup.wShowWindow = subprocess.SW_HIDE
                            julius_adingui  = subprocess.Popen([adintool_gui, '-in', 'mic', \
                                              '-rewind', julius_rewind, '-headmargin', julius_headmg, '-tailmargin', julius_tailmg, \
                                              '-lv', str(micLevel), '-zmean', ], \
                                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                                              #stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startup)
                            julius_beatgui  = time.time()

                        now=datetime.datetime.now()
                        stamp=now.strftime('%Y%m%d-%H%M%S')
                        voicef = 'temp/voices/' + stamp + '_voice.wav'

                        julius_hit_file = ''
                        if julius_hit_file == '':
                            if os.path.exists(julius_file2):
                                julius_hit_file = julius_file2
                                if julius_hit_sec > julius_sec:
                                    julius_hit_sec = julius_sec
                                try:
                                    os.rename(julius_file2, voicef)
                                    break
                                except:
                                   pass
                        if julius_hit_file == '':
                            if os.path.exists(julius_file1):
                                julius_hit_file = julius_file1
                                if julius_hit_sec > julius_sec:
                                    julius_hit_sec = julius_sec
                                try:
                                    os.rename(julius_file1, voicef)
                                    break
                                except:
                                    pass
                        if julius_hit_file == '':
                            if os.path.exists(julius_file):
                                julius_hit_file = julius_file
                                if julius_hit_sec > julius_sec:
                                    julius_hit_sec = julius_sec
                                try:
                                    os.rename(julius_file, voicef)
                                    break
                                except:
                                    pass

                        if not julius_adingui is None and os.name == 'nt':
                            if int(time.time() - julius_beatgui) >= 1:
                                try:
                                    hWnd = ctypes.windll.user32.FindWindowW('SDL_app',None)
                                    if hWnd is not 0:
                                        if julius_hit_file != '' or micguide == 'off':
                                            ctypes.windll.user32.ShowWindow(hWnd, 1)
                                            ctypes.windll.user32.SetForegroundWindow(hWnd)
                                        else:
                                            ctypes.windll.user32.ShowWindow(hWnd, 2)
                                except:
                                    pass

                        stamp  = ''
                        voicef = ''
                        time.sleep(0.1)
                        julius_sec = int(time.time() - wait_start)

                if listner == 'sr':
                    qLogOutput('input___:☆Listning...(' + inpLang + ')')
                    try:
                        with sr.Microphone(int(micdev)) as source:
                            try:
                                #speech = srr.listen(source, timeout=5, phrase_time_limit=10)
                                speech = srr.listen(source, timeout=5, phrase_time_limit=5)
                                data    =speech.get_wav_data(16000,2)

                                now=datetime.datetime.now()
                                stamp=now.strftime('%Y%m%d-%H%M%S')
                                voicef = 'temp/voices/' + stamp + '_voice.wav'
                                wb = open(voicef, 'wb')
                                wb.write(data)
                                wb.close
                                wb = None

                                srr.dynamic_energy_threshold = True
                                srr.adjust_for_ambient_noise(source, duration=1)
                            except:
                                srr.dynamic_energy_threshold = True
                                srr.adjust_for_ambient_noise(source, duration=5)
                                stamp  = ''
                                voicef = ''
                    except:
                        pass

                if listner == 'julius':
                    if voicef == '':
                        m = int(micLevel)
                        if julius_hit_sec <= 3 and m < 4444:
                            m = int(m * 1.3)
                            if m > 4444:
                                m = 4444
                            if m != int(micLevel):
                                qLogOutput('input___:micLevel changed ' + str(micLevel) + ' → ' + str(m))
                                micLevel = m

                if voicef != '':
                    rb = open(voicef, 'rb')
                    datasize = sys.getsizeof(rb.read())
                    rb.close
                    rb = None
                    qLogOutput('input___: ' + str(datasize) + ' byte')
                    if datasize<30000 or datasize>500000:
                        if listner != 'julius':
                            os.remove(voicef)
                            #stamp  = ''
                            voicef = ''
                        if listner == 'julius':
                            m = int(micLevel)
                            if datasize<30000 and m >= 500:
                                if m == 500:
                                    m = 2000
                                m = int(m * 0.90)
                                if m < 500:
                                    m = 500
                                if m != int(micLevel):
                                    qLogOutput('input___:micLevel changed ' + str(micLevel) + ' → ' + str(m))
                                    micLevel = m
                            if datasize>500000 and m <= 4444:
                                if m == 4444:
                                    m = 1000
                                m = int(m * 1.3)
                                if m > 4444:
                                    m = 4444
                                if m != int(micLevel):
                                    qLogOutput('input___:micLevel changed ' + str(micLevel) + ' → ' + str(m))
                                    micLevel = m

                if voicef != '':
                    if micON != 'None' and not os.path.exists(micON):
                        qLogOutput('input___:Synchronize(' + micON + ')...pass')
                        os.remove(voicef)
                        #stamp  = ''
                        voicef = ''

                if voicef != '':
                    voicef2 = 'temp/voices/' + stamp + '_voice2.wav'
                    try:
                        if runmode != 'number':
                            #sox = subprocess.Popen(['sox', voicef, '-r', '16000', '-b', '16', '-c', '1', voicef2, '-q', \
                            #                        'equalizer', '800', '1.0q', '7', ])
                            sox = subprocess.Popen(['sox', voicef, '-r', '16000', '-b', '16', '-c', '1', voicef2, '-q', ])
                        else:
                            #sox = subprocess.Popen(['sox', voicef, '-r', '16000', '-b', '16', '-c', '1', voicef2, '-q', \
                            #                        'equalizer', '800', '1.0q', '7', 'tempo', '0.9', ])
                            sox = subprocess.Popen(['sox', voicef, '-r', '16000', '-b', '16', '-c', '1', voicef2, '-q', ])
                        sox.wait()
                        sox.terminate()
                        sox = None
                        os.remove(voicef)
                        os.rename(voicef2, voicef)
                    except:
                        voicef = ''

                if voicef == '':
                    inpBusy = False
                    inpLast = time.time()

                    cn_s.put(['NG', ''])
                    if stamp != '':
                        qPlay('_ng', outputQ=None)

                else:
                    qLogOutput('input___:accepting...')
                    inpBusy = False
                    inpLast = time.time()

                    cn_s.put(['stamp',  stamp])
                    cn_s.put(['voicef', voicef])
                    qPlay('_accept', outputQ=None)

                if not julius_adingui is None:
                    try:
                        julius_adingui.wait(0.05)
                        julius_adingui = None
                    except:
                        pass

                if not julius_adingui is None and os.name == 'nt':
                    if int(time.time() - julius_beatgui) >= 1:
                        try:
                            hWnd = ctypes.windll.user32.FindWindowW('SDL_app',None)
                            if hWnd is not 0:
                                ctypes.windll.user32.ShowWindow(hWnd, 2)
                        except:
                            pass

                if not julius_adingui is None:
                    #if mictype != 'usb':
                        julius_adingui.terminate()
                        stdout, stderr  = julius_adingui.communicate()
                        julius_adingui  = None

                if not julius_adintool is None:
                        julius_adintool.terminate()
                        stdout, stderr  = julius_adintool.communicate()
                        julius_adintool = None

                time.sleep(2)

        inpBusy = False

        if cn_r.qsize() == 0:
            time.sleep(0.03)

    qLogOutput('input___:terminate')

    if not julius_adintool is None:
        try:
            julius_adintool.terminate()
            julius_adintool = None
        except:
            pass
    if not julius_adingui is None:
        try:
            julius_adingui.terminate()
            julius_adingui = None
        except:
            pass

    while cn_r.qsize() > 0:
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass

    qLogOutput('input___:end')



compute_beat=0
julius=None
def sub_compute(cn_r, cn_s, outputQ=None, ):
    global compute_beat
    global julius

    global inpApi
    global trnApi
    global outApi
    global inpLang
    global trnLang
    global outLang
    global txtLang
    global micLevel

    global compBusy
    global compLast

    qLogOutput('compute_:init')

    runmode  = cn_r.get()
    micdev   = cn_r.get()
    mictype  = cn_r.get()
    micguide = cn_r.get()
    recSJISf = cn_r.get()
    extpgm   = cn_r.get()
    cn_r.task_done()

    qLogOutput('compute_:runmode =' + str(runmode ))
    qLogOutput('compute_:micdev  =' + str(micdev  ))
    qLogOutput('compute_:mictype =' + str(mictype ))
    qLogOutput('compute_:micguide=' + str(micguide))
    qLogOutput('compute_:recSJISf=' + str(recSJISf))
    qLogOutput('compute_:extpgm  =' + str(extpgm  ))

    feedback  = False
    miss_beat = 0

    if (julius is None) and ((inpApi == 'julius') or (str(micdev).lower() != 'file')):
    #if (julius is None):
        if runmode == 'number':
            julius=subprocess.Popen(['julius/julius.exe', '-input', 'adinnet', '-adport', '5538', \
                                     '-C', 'julius/_jconf_20180313dnn999.jconf', '-dnnconf', 'julius/julius.dnnconf', \
                                     '-charconv', 'utf-8', 'sjis', '-logfile', 'temp/temp_julius.log', '-quiet', ], \
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, )
        else:
            julius=subprocess.Popen(['julius/julius.exe', '-input', 'adinnet', '-adport', '5538', \
                                     '-C', 'julius/_jconf_20180313dnn.jconf', '-dnnconf', 'julius/julius.dnnconf', \
                                     '-charconv', 'utf-8', 'sjis', '-logfile', 'temp/temp_julius.log', '-quiet', ], \
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, )
            chktime = time.time()
            chkhit  = ''
            while (int(time.time() - chktime) < 5):
                t = julius.stdout.readline()
                t = t.replace('\r', '')
                t = t.replace('\n', '')
                qLogOutput('julius:' + str(t), False)
                #qLogOutput('julius:' + str(t))
                if t != '':
                    chkhit = t
                else:
                    if chkhit != '':
                        break
                time.sleep(0.01)
                chktime = time.time()

    qLogOutput('compute_:start')

    while True:
        compute_beat = time.time()

        if cn_r.qsize() > 0:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if mode_get is None:
                qLogOutput('compute_:None=break')
                break

            if mode_get == 'stamp':
                stamp    = data_get
                cn_r_get = cn_r.get()
                dummy    = cn_r_get[0]
                recVoice = cn_r_get[1]
                cn_r.task_done()

            if cn_r.qsize() != 0 or cn_s.qsize() > 2:
                qLogOutput('compute_: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if mode_get != 'stamp':
                cn_s.put(['PASS', ''])
            else:

                compBusy = 'feedback play'
                compLast = time.time()

                if feedback == True:
                    qLogOutput('compute_:feedback playing...')
                    qPlay(recVoice, outputQ=outputQ)

                compBusy = 'recognition (1)'
                compLast = time.time()

                jultxt=''
                inptxt=''
                if julius is None:
                    if inpApi != 'free':
                        jultxt = qVoiceInput(useApi='free', inpLang=inpLang, \
                                             waveFile=recVoice, outputQ=outputQ)
                        if jultxt != '':
                            qLogOutput(stamp + ' Recognition  [' + jultxt + '] (free)')
                    else:
                        jultxt = '!'
                else:
                    tempList = 'temp/temp_juliuslist.txt'
                    tl = codecs.open(tempList, 'w', 'utf-8')
                    tl.write(recVoice.replace('\\','/') + '\n')
                    tl.close()
                    tl = None

                    adintool=subprocess.Popen(['julius/adintool.exe', '-input', 'file', '-filelist', tempList, \
                                               '-out', 'adinnet', '-server', 'localhost', '-port', '5538', '-nosegment',], \
                                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    adintool.wait()
                    adintool.terminate()
                    stdout, stderr = adintool.communicate()
                    adintool= None

                    jultxt = ''
                    chktime = time.time()
                    while True:
                        t = julius.stdout.readline()
                        t = t.replace('\r', '')
                        t = t.replace('\n', '')
                        qLogOutput('julius:' + str(t), False)
                        #qLogOutput('julius:' + str(t))
                        if t != '':
                            if t[:15]=='<search failed>':
                                jultxt = ' '
                            if t[:10]=='sentence1:':
                                jultxt = t[10:]
                        else:
                            if jultxt != '':
                                break
                        time.sleep(0.01)
                        chktime = time.time()

                    jultxt = jultxt.strip()
                    jultxt = jultxt.replace(u'　', '')
                    jultxt = jultxt.replace(' ', '')
                    if len(jultxt) > 0:
                        if jultxt[len(jultxt)-1:len(jultxt)] == u'。':
                            jultxt = jultxt[0:len(jultxt)-1]

                    if jultxt != '':
                        qLogOutput(stamp + ' Recognition  [' + jultxt + '] (julius)')

                if jultxt != '':
                    compBusy = 'recognition (2)'
                    compLast = time.time()

                    if inpApi == 'julius':
                        if jultxt != '!':
                            inptxt = jultxt
                    else:
                        inptxt=qVoiceInput(useApi=inpApi, inpLang=inpLang, \
                                           waveFile=recVoice, outputQ=outputQ)

                        if inptxt != '':
                            if inptxt[0:9] != '!Google, ':
                                qLogOutput(stamp + ' Recognition  [' + inptxt + '] (' + inpApi + ')')
                            else:
                                inptxt = inptxt[9:]
                                qLogOutput(stamp + ' Recognition  [' + inptxt + '] (!Google)')
                        else:
                            if jultxt != '!':
                                inptxt = jultxt

                if inptxt == '':
                    os.remove(recVoice)
                    qLogOutput(stamp + ' ! ')
                    if micguide != 'off':
                        qPlay('_ng', outputQ=outputQ)

                    if 1==1:
                        if recSJISf == 'Default':
                            recTextx = 'temp/temp_recSJIS.txt'
                        else:
                            recTextx = recSJISf
                        try:
                            w = codecs.open(recTextx, 'w', 'shift_jis')
                            w.write('')
                            w.close()
                            w = None
                        except:
                            w = None

                trntxt=''
                if inptxt != '':
                    compBusy = 'recognition (3)'
                    compLast = time.time()

                    txt = inptxt
                    if runmode == 'number':
                        txt = txt.replace(u'ゼロ', '0')
                        txt = txt.replace(u'０',   '0')
                        txt = txt.replace(u'１',   '1')
                        txt = txt.replace(u'２',   '2')
                        txt = txt.replace(u'３',   '3')
                        txt = txt.replace(u'４',   '4')
                        txt = txt.replace(u'５',   '5')
                        txt = txt.replace(u'６',   '6')
                        txt = txt.replace(u'７',   '7')
                        txt = txt.replace(u'８',   '8')
                        txt = txt.replace(u'９',   '9')
                        if txt.isdigit():
                            trntxt = txt
                        else:
                            txt = txt.replace('0',   'ゼロ')

                    if runmode == 'speech':
                            trntxt = txt

                    if trntxt == '':
                        trntxt=qTranslator(useApi=trnApi, inpLang=inpLang, outLang=trnLang,
                                           transText=txt, outputQ=outputQ)
                        if trntxt != '':
                            if trntxt[0:9] != '!Google, ':
                                qLogOutput(stamp + ' Translation  [' + trntxt + '] (' + trnApi + ')')
                            else:
                                trntxt = trntxt[9:]
                                qLogOutput(stamp + ' Translation  [' + trntxt + '] (!Google)')
                            #qPlay('_ok', outputQ=outputQ)

                    if trntxt == '':
                        os.remove(recVoice)
                        qLogOutput(stamp + ' ! ')
                        if micguide != 'off':
                            qPlay('_ng', outputQ=outputQ)

                        if recSJISf == 'Default':
                            recTextx = 'temp/temp_recSJIS.txt'
                        else:
                            recTextx = recSJISf
                        try:
                            w = codecs.open(recTextx, 'w', 'shift_jis')
                            w.write('')
                            w.close()
                            w = None
                        except:
                            w = None

                        sec = int(time.time() - miss_beat)
                        miss_beat = time.time()
                        if int(micLevel) != 0:
                            m = int(micLevel)
                            if sec>120 and m >= 500:
                                    if m == 500:
                                        m = 2000
                                    m = int(m * 0.90)
                                    if m < 500:
                                        m = 500
                                    if m != int(micLevel):
                                        qLogOutput('compute_:micLevel changed ' + str(micLevel) + ' → ' + str(m))
                                        micLevel = m
                            if sec<120 and m <= 4444:
                                    if m == 4444:
                                        m = 1000
                                    m = int(m * 1.3)
                                    if m > 4444:
                                        m = 4444
                                    if m != int(micLevel):
                                        qLogOutput('compute_:micLevel changed ' + str(micLevel) + ' → ' + str(m))
                                        micLevel = m

                if trntxt != '':
                    if runmode == 'number' or runmode == 'numeric':
                        trntxt = trntxt.lower()
                        if trntxt[len(trntxt)-1:] == '.':
                            trntxt = trntxt[0:len(trntxt)-1]

                        num = trntxt.lower()
                        num = num.replace(u'０', '0')
                        num = num.replace('zero', '0')
                        num = num.replace('one', '1')
                        num = num.replace('two', '2')
                        num = num.replace('three', '3')
                        num = num.replace('four', '4')
                        num = num.replace('five', '5')
                        num = num.replace('six', '6')
                        num = num.replace('seven', '7')
                        num = num.replace('eight', '8')
                        num = num.replace('nine', '9')
                        num = num.replace(' ', '')
                        num = num.replace(',', '')

                        if num != '' and num != trntxt and num.isdigit():
                            qLogOutput(stamp + ' ' + trntxt + ' -> ' + str(num))
                            trntxt = str(num)

                if trntxt != '':
                    compBusy = 'file output'
                    compLast = time.time()

                    if inpLang=='ja':
                        recSJISx = 'temp/voices/' + stamp + '_sjis.txt'
                        try:
                            w = codecs.open(recSJISx, 'w', 'shift_jis')
                            w.write(inptxt)
                            w.close()
                            w = None
                        except:
                            w = None

                    recText1 = 'temp/voices/' + stamp + '_text_' + inpLang + '.txt'
                    try:
                        w = codecs.open(recText1, 'w', 'utf-8')
                        w.write(inptxt)
                        w.close()
                        w = None
                    except:
                        w = None

                    recTran1 = 'temp/voices/' + stamp + '_text_' + trnLang + '.txt'
                    try:
                        w = codecs.open(recTran1, 'w', 'utf-8')
                        w.write(trntxt)
                        w.close()
                        w = None
                    except:
                        w = None

                    if extpgm != 'None':
                        if os.path.exists(extpgm):
                            #os.system(extpgm + ' ' + stamp)
                            p=subprocess.Popen([extpgm, stamp])
                            #p.wait()

                    recVoice2 = 'temp/temp_recVoice.wav'
                    try:
                        wb = open(recVoice2, 'wb')
                        wb.write(voice)
                        wb.close
                        wb = None
                    except:
                        wb = None

                    recTran2 = 'temp/temp_recTranslator.txt'
                    try:
                        w = codecs.open(recTran2, 'w', 'utf-8')
                        w.write(trntxt)
                        w.close()
                        w = None
                    except:
                        w = None

                    recText2 = 'temp/temp_recUTF8.txt'
                    try:
                        w = codecs.open(recText2, 'w', 'utf-8')
                        w.write(inptxt)
                        w.close()
                        w = None
                    except:
                        w = None

                    if recSJISf == 'Default':
                        recTextx = 'temp/temp_recSJIS.txt'
                    else:
                        recTextx = recSJISf

                    try:
                        w = codecs.open(recTextx, 'w', 'shift_jis')
                        w.write(inptxt)
                        w.close()
                        w = None
                    except:
                        w = None
                        try:
                            w2 = codecs.open(recTextx, 'w', 'utf-8')
                            w2.write(inptxt)
                            w2.close()
                            w2 = None
                        except:
                            w2 = None

                if trntxt != '':
                    compBusy = 'processing'
                    compLast = time.time()

                    txt = inptxt

                    if inptxt == u'バルス' or inptxt == u'システム シャットダウン' or \
                       trntxt.lower() == 'system shutdown':
                        txt = u'システムシャットダウン'

                    if inptxt == u'今何時' or inptxt == u'今 何時':
                        now2=datetime.datetime.now()
                        txt  = u'現在の時刻は、'
                        txt += now2.strftime('%H') + u'時'
                        txt += now2.strftime('%M') + u'分です'

                    if inptxt == u'フィードバック' or inptxt == u'デバッグ' or \
                       trntxt.lower() == 'feedback' or trntxt.lower() == 'debug':
                        if feedback != True:
                            feedback = True
                            txt = u'音声フィードバック開始します'
                        else:
                            feedback = False
                            txt = u'音声フィードバック終了します'

                    if inptxt == u'ワトソン' or inptxt == u'Ｗａｔｓｏｎ' or inptxt.lower() == 'watson' or \
                       inptxt == u'アイビーエム' or inptxt.lower() == 'ibm' or \
                       trntxt.lower() == 'watson' or trntxt.lower() == 'ibm':
                        txt  = u'AIを IBM Watson に切り替えます'
                    if inptxt == u'グーグル' or inptxt == u'Ｇｏｏｇｌｅ' or inptxt == u'ｇｏｏｇｌｅ' or \
                       inptxt.lower() == 'google' or trntxt.lower() == 'google':
                        txt  = u'AIを Google に切り替えます'
                    if inptxt == u'アジュール' or inptxt == u'Ａｚｕｒｅ' or inptxt.lower() == 'azure' or \
                       inptxt == u'マイクロソフト' or inptxt.lower() == 'microsoft' or \
                       trntxt.lower() == 'azure' or trntxt.lower() == 'microsoft':
                        txt = u'AIを Microsoft Azure に切り替えます'

                    if txt != inptxt:
                        trntxt=qTranslator(useApi=trnApi, inpLang=inpLang, outLang=trnLang,
                                   transText=txt, outputQ=outputQ)
                        if trntxt != '':
                            qVoiceOutput(useApi=outApi, outLang=outLang, outText=trntxt,outputQ=outputQ)

                if trntxt != '':
                    if inptxt == u'バルス' or inptxt == u'システム シャットダウン' or \
                       inptxt == u'システムシャットダウン' or trntxt.lower() == 'system shutdown':
                        cn_s.put(['END', ''])
                        break

                    if inptxt == u'今何時' or inptxt == u'今 何時' or \
                       inptxt == u'フィードバック' or inptxt == u'デバッグ' or \
                       trntxt.lower() == 'feedback' or trntxt.lower() == 'debug':
                        trntxt = ''

                    if inptxt == u'ワトソン' or inptxt == u'Ｗａｔｓｏｎ' or inptxt.lower() == 'watson' or \
                       inptxt == u'アイビーエム' or inptxt.lower() == 'ibm' or \
                       trntxt.lower() == 'watson' or trntxt.lower() == 'ibm':
                        inpApi = 'watson'
                        trnApi = 'watson'
                        outApi = 'watson'
                        if runmode == 'translator' or runmode == 'learning':
                            qVoiceApiInfo(trnApi=trnApi, outputQ=outputQ)
                        trntxt = ''

                    if inptxt == u'グーグル' or inptxt == u'Ｇｏｏｇｌｅ' or inptxt == u'ｇｏｏｇｌｅ' or \
                       inptxt.lower() == 'google' or trntxt.lower() == 'google':
                        inpApi = 'google'
                        trnApi = 'google'
                        outApi = 'google'
                        if runmode == 'translator' or runmode == 'learning':
                            qVoiceApiInfo(trnApi=trnApi, outputQ=outputQ)
                        trntxt = ''

                    if inptxt == u'アジュール' or inptxt == u'Ａｚｕｒｅ' or inptxt.lower() == 'azure' or \
                       inptxt == u'マイクロソフト' or inptxt.lower() == 'microsoft' or \
                       trntxt.lower() == 'azure' or trntxt.lower() == 'microsoft':
                        inpApi = 'azure'
                        trnApi = 'azure'
                        outApi = 'azure'
                        if runmode == 'translator' or runmode == 'learning':
                            qVoiceApiInfo(trnApi=trnApi, outputQ=outputQ)
                        trntxt = ''

                if trntxt != '':
                    if runmode == 'translator' or runmode == 'learning':
                        compBusy = 'translator'
                        compLast = time.time()

                        res = sub_compute_translator(runmode, stamp, inptxt, trntxt, outputQ,)

                if trntxt != '':
                    cn_s.put(['OK', ''])
                else:
                    cn_s.put(['NG', ''])

        compBusy = False

        if cn_r.qsize() == 0:
            time.sleep(0.03)

    qLogOutput('compute_:terminate')

    if not julius is None:
        try:
            #julius.wait()
            julius.terminate()
            stdout, stderr = julius.communicate()
            julius = None
        except:
            pass

    while cn_r.qsize() > 0:
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass

    qLogOutput('compute_:end')



def sub_compute_translator(runmode, stamp, inptxt, trntxt, outputQ=None,):
    global inpApi
    global trnApi
    global outApi
    global inpLang
    global trnLang
    global outLang
    global txtLang

    if inptxt != '':
        txt=inptxt
        lng=trnLang

        if inptxt == u'リセット' or inptxt == 'reset':
            txt = u'設定をリセットします'
            inpApi  = 'google'
            inpLang = 'ja'
            trnApi  = 'azure'
            trnLang = 'en'
            outApi  = 'watson'
            outLang = 'en'

        if inptxt == u'スワップ' or inptxt == 'swap':
            txt = u'翻訳音声を入れ替えます'
            trnLang = inpLang
            outLang = inpLang
            inpLang = lng

        if inptxt == u'何語' or inptxt == u'何語ですか' or inptxt == u'何語 ですか':
            txt  = u'この機能は、'
            txt += u'日本語、英語、アラビア語、スペイン語、ドイツ語、フランス語、'
            txt += u'イタリア語、ポルトガル語、ロシア語、トルコ語、ウクライナ語、'
            txt += u'中国語ならびに韓国語'
            txt += u'に翻訳できます。あなたは何語を話しますか？'

        if inptxt == u'日本語':
            trnLang = 'ja'
            outLang = trnLang
            qLogOutput('compute_:outLang=' + str(outLang))
        if inptxt == u'英語':
            trnLang = 'en'
            outLang = trnLang
            qLogOutput('compute_:outLang=' + str(outLang))
        if inptxt == u'アラビア語' or inptxt == u'アラビア 語':
            trnLang = 'ar'
            outLang = trnLang
            qLogOutput('compute_:outLang=' + str(outLang))
        if inptxt == u'スペイン語' or inptxt == u'スペイン 語':
            trnLang = 'es'
            outLang = trnLang
            qLogOutput('compute_:outLang=' + str(outLang))
        if inptxt == u'ドイツ語' or inptxt == u'ドイツ 語':
            trnLang = 'de'
            outLang = trnLang
            qLogOutput('compute_:outLang=' + str(outLang))
        if inptxt == u'フランス語' or inptxt == u'フランス 語':
            trnLang = 'fr'
            outLang = trnLang
            qLogOutput('compute_:outLang=' + str(outLang))
        if inptxt == u'イタリア語' or inptxt == u'イタリア 語':
            trnLang = 'it'
            outLang = trnLang
            qLogOutput('compute_:outLang=' + str(outLang))
        if inptxt == u'ポルトガル語' or inptxt == u'ポルトガル 語':
            trnLang = 'pt'
            outLang = trnLang
            qLogOutput('compute_:outLang=' + str(outLang))
        if inptxt == u'ロシア語' or inptxt == u'ロシア 語':
            trnLang = 'ru'
            outLang = trnLang
            qLogOutput('compute_:outLang=' + str(outLang))
        if inptxt == u'トルコ語' or inptxt == u'トルコ 語':
            trnLang = 'tr'
            outLang = trnLang
            qLogOutput('compute_:outLang=' + str(outLang))
        if inptxt == u'ウクライナ語' or inptxt == u'ウクライナ 語':
            trnLang = 'uk'
            outLang = trnLang
            qLogOutput('compute_:outLang=' + str(outLang))
        if inptxt == u'中国語'or inptxt == u'中国 語':
            trnLang = 'zh-CN'
            outLang = trnLang
            qLogOutput('compute_:outLang=' + str(outLang))
        if inptxt == u'韓国語' or inptxt == u'韓国 語':
            trnLang = 'ko'
            outLang = trnLang
            qLogOutput('compute_:outLang=' + str(outLang))

        if txt != inptxt or lng != trnLang:
            trntxt=qTranslator(useApi=trnApi, inpLang=inpLang, outLang=trnLang,
                               transText=txt, outputQ=outputQ)

    if trntxt != '':
        outtxt = trntxt

        qLogOutput(stamp + ' Vocalization [' + outtxt + '] (' + outApi + ')')
        outVoice = 'temp/voices/' + stamp + '_voice_' + outLang + '.mp3'

        res = qVoiceOutput(useApi=outApi, outLang=outLang, outText=outtxt,
                           tempFile=outVoice, outputQ=outputQ)
        if res[0:9] == '!Google, ':
            qLogOutput(stamp + ' Vocalization [' + outtxt + '] (!Google)')

    if trntxt != '' and runmode == 'learning':

        qLogOutput(stamp + ' Vocalization [' + inptxt + '] (' + outApi + ')')
        outVoice = 'temp/voices/' + stamp + '_voice_' + inpLang + '.mp3'

        res = qVoiceOutput(useApi=outApi, outLang=inpLang, outText=inptxt,
                           tempFile=outVoice, outputQ=outputQ)
        if res[0:9] == '!Google, ':
            qLogOutput(stamp + ' Vocalization [' + inptxt + '] (!Google)')

    if inptxt == u'リセット' or inptxt == 'reset':
        qVoiceApiInfo(inpApi=inpApi, trnApi=trnApi, outApi=outApi, outputQ=outputQ)



output_beat=0
def sub_output(cn_r,cn_s):
    global output_beat

    global inpApi
    global trnApi
    global outApi
    global inpLang
    global trnLang
    global outLang
    global txtLang

    global outBusy
    global outLast

    qLogOutput('output__:init')

    runmode = cn_r.get()
    micdev  = cn_r.get()
    mictype = cn_r.get()
    micguide= cn_r.get()
    cn_r.task_done()

    qLogOutput('output__:runmode =' + str(runmode ))
    qLogOutput('output__:micdev  =' + str(micdev  ))
    qLogOutput('output__:mictype =' + str(mictype ))
    qLogOutput('output__:micguide=' + str(micguide))

    qLogOutput('output__:start')

    while True:
        output_beat = time.time()

        if cn_r.qsize() > 0:
            cn_s.put(['BUSY', ''])

            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if mode_get is None:
                qLogOutput('output__:None=break')
                break

            if cn_r.qsize() > 2 or cn_s.qsize() > 4:
                qLogOutput('output__: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            file = ''
            if mode_get == 'file':
                outBusy = 'Playing'
                outLast = time.time()

                file = data_get
                #qLogOutput('output__:' + file)
                qPlay(file, outputQ=None, sync=True)

                outBusy = False
                outLast = time.time()

            cn_s.put(['OK', file])

        outBusy = False

        if cn_r.qsize() == 0:
            time.sleep(0.03)

    qLogOutput('output__:terminate')

    while cn_r.qsize() > 0:
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass
    while cn_s.qsize() > 0:
        try:
            cn_s_get = cn_s.get()
            mode_get = cn_s_get[0]
            data_get = cn_s_get[1]
            cn_s.task_done()
        except:
            pass

    qLogOutput('output__:end')



playtext_beat=0
def sub_playtext(cn_r,cn_s,outputQ=None):
    global playtext_beat

    global inpApi
    global trnApi
    global outApi
    global inpLang
    global trnLang
    global outLang
    global txtLang

    global playBusy
    global playLast

    qLogOutput('playtext:init')

    runmode = cn_r.get()
    micdev  = cn_r.get()
    mictype = cn_r.get()
    micguide= cn_r.get()
    cn_r.task_done()

    qLogOutput('playtext:runmode =' + str(runmode ))
    qLogOutput('playtext:micdev  =' + str(micdev  ))
    qLogOutput('playtext:mictype =' + str(mictype ))
    qLogOutput('playtext:micguide=' + str(micguide))

    qLogOutput('playtext:start')

    while True:
        playtext_beat = time.time()

        if cn_r.qsize() > 0:
            cn_s.put(['BUSY', ''])

            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if mode_get is None:
                qLogOutput('playtext:None=break')
                break

            if cn_r.qsize() != 0 or cn_s.qsize() > 4:
                qLogOutput('playtext: queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            if mode_get != 'PASS':

                # file check

                playFile1='temp/temp_playSJIS.txt'
                playFile2='temp/@temp_playSJIS.txt'
                if os.path.exists(playFile1):
                    #qLogOutput('playtext:' + playFile1)
                    if os.path.exists(playFile2):
                        try:
                            os.remove(playFile2)
                        except:
                            pass
                    if not os.path.exists(playFile2):
                        try:
                            os.rename(playFile1, playFile2)

                            textBusy = 'Text Accept'
                            textLast = time.time()

                            try:
                                txt = ''
                                rt = codecs.open(playFile2, 'r', 'shift_jis')
                                for t in rt:
                                    txt = (txt + ' ' + str(t)).strip()
                                rt.close
                                rt = None
                                os.remove(playFile2)

                                if txt == '_ok' or txt == '_ng' or \
                                   txt == '_ready' or txt == '_accept' or \
                                   txt == '_shutter':
                                    textBusy = 'Text Playing'
                                    textLast = time.time()

                                    outputQ.put(['file', txt])
                                    outputQ.put(['file', '_!playing'])
                                    qLogOutput('playtext:BGM=' + txt)

                                    textBusy = False
                                    textLast = time.time()

                                else:
                                    outtxt = txt
                                    if txtLang != outLang:
                                        textBusy = 'Text Translation'
                                        textLast = time.time()

                                        outtxt=qTranslator(useApi=trnApi, inpLang=txtLang, outLang=outLang,
                                                           transText=txt, outputQ=outputQ)
                                        qLogOutput('playtext: Translation  [' + txt + '] (' + trnApi + ')')

                                    textBusy = 'Text Vocalization'
                                    textLast = time.time()

                                    qVoiceOutput(useApi=outApi, outLang=outLang, outText=outtxt, outputQ=outputQ)
                                    qLogOutput('playtext: Vocalization [' + outtxt + '] (' + outApi + ')')

                                    textBusy = False
                                    textLast = time.time()

                            except:
                                rt = None

                            textBusy = False
                            textLast = time.time()

                        except:
                            pass

            cn_s.put(['OK', ''])

        textBusy = False

        if cn_r.qsize() == 0:
            time.sleep(0.5)

    qLogOutput('playtext:terminate')

    while cn_r.qsize() > 0:
        try:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
        except:
            pass
    while cn_s.qsize() > 0:
        try:
            cn_s_get = cn_s.get()
            mode_get = cn_s_get[0]
            data_get = cn_s_get[1]
            cn_s.task_done()
        except:
            pass

    qLogOutput('playtext:end')



inpApi   = 'free'
trnApi   = 'free'
outApi   = 'free'
if os.name == 'nt':
    outApi   = 'win32'
inpLang  = 'ja'
trnLang  = 'en'
outLang  = 'en'
txtLang  = 'ja'
micLevel = '777'

inpBusy  = False
inpLast  = 0
compBusy = False
compLast = 0
textBusy = False
textLast = 0
outBusy  = False
outLast  = 0
playBusy = False
playLast = 0

main_beat=0
if __name__ == '__main__':
    #global main_beat
    #global output_beat
    #global compute_beat
    #global input_beat
    #global playtext_beat

    #global inpApi
    #global trnApi
    #global outApi
    #global inpLang
    #global trnLang
    #global outLang
    #global txtLang
    #global micLevel

    #global inpBusy
    #global inpLast
    #global compBusy
    #global compLast
    #global textBusy
    #global textLast
    #global outBusy
    #global outLast
    #global playBusy
    #global playLast

    qLogOutput('__main__:init')
    qLogOutput('__main__:exsample.py micdev, mictype, micLevel, micguide, api, input-lang, output-lang, textif-lang, runmode, mic-syncf, recSJISf, extpgm,')
    #runmode translator,learning,speech,number

    recSJIS ='temp/temp_recSJIS.txt'
    recUTF8 ='temp/temp_recUTF8.txt'
    recTrans='temp/temp_recTranslator.txt'
    if os.path.exists(recSJIS):
        os.remove(recSJIS)
    if os.path.exists(recUTF8):
        os.remove(recUTF8)
    if os.path.exists(recTrans):
        os.remove(recTrans)

    micdev   = '0'
    mictype  = 'bluetooth'
    micguide = 'on'
    runmode  = 'translator'
    micON    = 'None'
    recSJISf = 'Default'
    extpgm   = 'None'
    if len(sys.argv)>=2:
        micdev   = sys.argv[1]
    if len(sys.argv)>=3:
        mictype  = str(sys.argv[2]).lower()
    if len(sys.argv)>=4:
        micLevel = sys.argv[3]
    if len(sys.argv)>=5:
        micguide = str(sys.argv[4]).lower()
    if len(sys.argv)>=6:
        if str(sys.argv[5]).lower() != inpApi:
            inpApi = str(sys.argv[5]).lower()
            if inpApi != 'julius':
                trnApi = inpApi
                outApi = inpApi
    if len(sys.argv)>=7:
        inpLang  = sys.argv[6]
    if len(sys.argv)>=8:
        outLang  = sys.argv[7]
    if len(sys.argv)>=9:
        txtLang  = sys.argv[8]
    if len(sys.argv)>=10:
        runmode  = str(sys.argv[9]).lower()
    if len(sys.argv)>=11:
        micON    = sys.argv[10]
    if len(sys.argv)>=12:
        recSJISf = sys.argv[11]
    if len(sys.argv)>=13:
        extpgm   = sys.argv[12]
    if inpLang=='ja-JP':
        inpLang  = 'ja'
    if outLang=='en-US':
        outLang  = 'en'
    if txtLang=='ja-JP':
        txtLang  = 'ja'
    if inpLang=='ja' and outLang=='ja':
        trnLang  = 'en'
    if runmode == 'translator' or runmode == 'learning' or runmode == 'speech':
        trnLang  = outLang

    if recSJISf != 'Default':
        if os.path.exists(recSJISf):
            os.remove(recSJISf)

    qLogOutput('')
    qLogOutput('__main__:micdev  =' + str(micdev  ))
    qLogOutput('__main__:mictype =' + str(mictype ))
    qLogOutput('__main__:micLevel=' + str(micLevel))
    qLogOutput('__main__:micguide=' + str(micguide))
    qLogOutput('__main__:input   =' + str(inpLang ))
    qLogOutput('__main__:output  =' + str(outLang ))
    qLogOutput('__main__:text    =' + str(txtLang ))
    qLogOutput('__main__:mode    =' + str(runmode ))
    qLogOutput('__main__:micON   =' + str(micON   ))
    qLogOutput('__main__:recSJISf=' + str(recSJISf))
    qLogOutput('__main__:extpgm  =' + str(extpgm  ))

    qLogOutput('')
    qLogOutput('__main__:infomation')
    qLogOutput('[ keywords ]')
    qLogOutput(u'システムシャットダウン,')
    qLogOutput(u'今何時,フィードバック,')
    qLogOutput(u'ワトソン,グーグル,マイクロソフト,')
    if runmode == 'translator' or runmode == 'learning':
        qLogOutput('[ translator and learning ]')
        qLogOutput(u'リセット,スワップ,')
        qLogOutput(u'何語ですか,')
        qLogOutput(u'日本語、英語、アラビア語、スペイン語、ドイツ語、フランス語、')
        qLogOutput(u'イタリア語、ポルトガル語、ロシア語、トルコ語、ウクライナ語、')
        qLogOutput(u'中国語ならびに韓国語')

    qLogOutput('')
    qLogOutput('__main__:start')
    main_start   = time.time()
    main_beat    = 0

    output_s     = queue.Queue()
    output_r     = queue.Queue()
    output_proc  = None
    output_beat  = 0
    output_skip  = 0
    compute_s    = queue.Queue()
    compute_r    = queue.Queue()
    compute_proc = None
    compute_beat = 0
    input_s      = queue.Queue()
    input_r      = queue.Queue()
    input_proc   = None
    input_beat   = 0
    playtext_s   = queue.Queue()
    playtext_r   = queue.Queue()
    playtext_proc= None
    playtext_beat= 0
    playtext_skip= 0

    while True:
        main_beat = time.time()

        # Thread timeout check

        if (input_beat != 0):
            sec = int(time.time() - input_beat)
            if sec > 60:
                qLogOutput('__main__:input_proc 60s')
                #input_beat = time.time()
                qLogOutput('__main__:input_proc break')

                if str(micdev).lower() != 'file':
                    try:
                        dummy=subprocess.Popen(['taskkill', '/im', 'adintool-gui.exe', '/f',])
                        time.sleep(1.0)
                        dummy=subprocess.Popen(['taskkill', '/im', 'adintool.exe', '/f',])
                        time.sleep(1.0)
                    except:
                        pass

                input_s.put([None, None])
                time.sleep(3.0)
                input_proc = None
                input_beat = 0

                if not julius_adintool is None:
                    try:
                        julius_adintool.terminate()
                        julius_adintool = None
                    except:
                        pass
                if not julius_adingui is None:
                    try:
                        julius_adingui.terminate()
                        julius_adingui = None
                    except:
                        pass

        if (compute_beat != 0):
            sec = int(time.time() - compute_beat)
            if sec > 60:
                qLogOutput('__main__:compute_proc 60s')
                #compute_beat = time.time()
                qLogOutput('__main__:compute_proc break')
                compute_s.put([None, None])
                time.sleep(3.0)
                compute_proc = None
                compute_beat = 0

                if not julius is None:
                    try:
                        #julius.wait()
                        julius.terminate()
                        stdout, stderr = julius.communicate()
                        julius = None
                    except:
                        pass

        if (output_beat != 0):
            sec = int(time.time() - output_beat)
            if sec > 60:
                qLogOutput('__main__:output_proc 60s')
                #output_beat = time.time()
                qLogOutput('__main__:output_proc break')
                output_s.put([None, None])
                time.sleep(3.0)
                output_proc = None
                output_beat = 0
                output_skip = 0

        if (playtext_beat != 0):
            sec = int(time.time() - playtext_beat)
            if sec > 60:
                qLogOutput('__main__:playtext_proc 60s')
                #playtext_beat = time.time()
                qLogOutput('__main__:playtext_proc break')
                playtext_s.put([None, None])
                time.sleep(3.0)
                playtext_proc = None
                playtext_beat = 0
                playtext_skip = 0

        # Thread start

        if output_proc is None:
            while output_s.qsize() > 0:
                dummy = output_s.get()
            while output_r.qsize() > 0:
                dummy = output_r.get()
            output_proc = threading.Thread(target=sub_output, args=(output_s,output_r,))
            output_proc.daemon = True
            output_s.put(runmode )
            output_s.put(micdev  )
            output_s.put(mictype )
            output_s.put(micguide)
            output_proc.start()
            time.sleep(1.0)

            output_s.put(['START', ''])
            output_beat = 0
            output_skip = 0

        if compute_proc is None:
            while compute_s.qsize() > 0:
                dummy = compute_s.get()
            while compute_r.qsize() > 0:
                dummy = compute_r.get()
            compute_proc = threading.Thread(target=sub_compute, args=(compute_s,compute_r,output_s,))
            compute_proc.daemon = True
            compute_s.put(runmode )
            compute_s.put(micdev  )
            compute_s.put(mictype )
            compute_s.put(micguide)
            compute_s.put(recSJISf)
            compute_s.put(extpgm  )
            compute_proc.start()
            time.sleep(1.0)

            compute_s.put(['START', ''])
            compute_beat = 0

        if input_proc is None:
            while input_s.qsize() > 0:
                dummy = input_s.get()
            while input_r.qsize() > 0:
                dummy = input_r.get()
            input_proc = threading.Thread(target=sub_input, args=(input_s,input_r,output_s,output_r,playtext_s,playtext_r,))
            input_proc.daemon = True
            input_s.put(runmode )
            input_s.put(micdev  )
            input_s.put(mictype )
            input_s.put(micguide)
            input_s.put(micON   )
            input_s.put(recSJISf)
            input_proc.start()
            time.sleep(1.0)

            input_s.put(['START', ''])
            input_beat = 0

        if playtext_proc is None:
            while playtext_s.qsize() > 0:
                dummy = playtext_s.get()
            while playtext_r.qsize() > 0:
                dummy = playtext_r.get()
            playtext_proc = threading.Thread(target=sub_playtext, args=(playtext_s,playtext_r,output_s,))
            playtext_proc.daemon = True
            playtext_s.put(runmode )
            playtext_s.put(micdev  )
            playtext_s.put(mictype )
            playtext_s.put(micguide)
            playtext_proc.start()
            time.sleep(1.0)

            playtext_s.put(['START', ''])
            playtext_beat = 0
            playtext_skip = 0

        # processing

        if output_r.qsize() > 0:
            output_get = output_r.get()
            output_res = output_get[0]
            output_dat = output_get[1]
            output_r.task_done()
        if output_r.qsize() == 0 and output_s.qsize() == 0:
            output_skip += 1
        else:
            output_skip = 0
        if output_skip > 50:
            output_s.put(['RUN', ''])
            output_skip = 0

        if input_r.qsize() > 0:
            input_get = input_r.get()
            input_res = input_get[0]
            input_dat = input_get[1]
            input_r.task_done()
            if input_res == 'INIT':
                input_s.put(['INIT', ''])
            elif input_res == 'PASS':
                input_s.put(['READY', ''])
            elif input_res == 'NG':
                input_s.put(['NEXT', ''])
            else:
                stamp     = input_dat
                input_get = input_r.get()
                dummy     = input_get[0]
                voicef    = input_get[1]
                input_r.task_done()

                compute_s.put(['stamp',  stamp])
                compute_s.put(['voicef', voicef])
                if recSJISf != 'Default' or micON != 'None':
                    if compute_r.qsize() == 0:
                        chktime = time.time()
                        while (compute_r.qsize() == 0) and (int(time.time() - chktime) < 5):
                            time.sleep(0.1)

                input_s.put(['READY', ''])

        if compute_r.qsize() > 0:
            compute_get = compute_r.get()
            compute_res = compute_get[0]
            compute_dat = compute_get[1]
            compute_r.task_done()

            if compute_res == 'END':
                break

        if playtext_r.qsize() > 0:
            playtext_get = playtext_r.get()
            playtext_res = playtext_get[0]
            playtext_dat = playtext_get[1]
            playtext_r.task_done()
        if playtext_r.qsize() == 0 and playtext_s.qsize() == 0:
            playtext_skip += 1
        else:
            playtext_skip = 0
        if playtext_skip > 50:
            playtext_s.put(['RUN', ''])
            playtext_skip = 0

        time.sleep(0.01)



    qLogOutput('__main__:terminate')

    try:
        input_s.put(   [None, None])
        compute_s.put( [None, None])
        output_s.put(  [None, None])
        playtext_s.put([None, None])
    except:
        pass

    try:
        input_proc.join()
        compute_proc.join()
        output_proc.join()
        playtext_proc.join()
    except:
        pass

    qLogOutput('__main__:bye!')



