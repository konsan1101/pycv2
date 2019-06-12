#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import sys
import time
import codecs
import subprocess

#import contextlib
#with contextlib.redirect_stdout(None):
#    import pygame.mixer

from requests_toolbelt import SSLAdapter
import requests
import ssl
import wave
import numpy as np



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
    lng     = 'ja'
    txtFile = 'temp/temp_msg.txt'
    tmpFile = 'temp/temp_voice.wav' #Azure, HOYA
    #tmpFile = 'temp/temp_voice.mp3' #Google, Watson
    if len(sys.argv)>=2:
        lng = sys.argv[1]
    if len(sys.argv)>=3:
        txtFile = sys.argv[2]
    if len(sys.argv)>=4:
        tmpFile = sys.argv[3]
    if lng=='ja-JP':
        lng = 'ja'

    print('')
    print('speech_output_hoya.py')
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

        # HOYA
        payload = {
              'text': txt,
              'speaker': 'hikari',     # free! haruka,hikari,show,takeru,santa,bear
              'emotion': 'happiness',  # happiness,anger,sadness
              'emotion_level': 1,      # 1,2,3,4
              'pitch': 100,            # 50-200
              'speed': 120,            # 50-400
              'volume': 100,           # 50-200
              'format': 'wav'          # wav,ogg,aac
        }

        s = requests.Session()
        s.mount(   'https://api.voicetext.jp/v1/tts', SSLAdapter(ssl.PROTOCOL_TLSv1))
        r = s.post('https://api.voicetext.jp/v1/tts', params=payload, auth=('xx:',''))
        #print(' Status Code : ', r.status_code)
        if r.status_code != 200:
            print(' Error!', r.json()['error']['message'])
            sys.exit()

        wb = open(tmpFile, 'wb')
        wb.write(r.content)
        wb.close()
        wb = None

    except:
        print(' Error!', sys.exc_info()[0])
        sys.exit()

    if os.path.exists(tmpFile):
        qPlay(tmpFile)



