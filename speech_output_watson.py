#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import codecs
import subprocess

#import contextlib
#with contextlib.redirect_stdout(None):
#    import pygame.mixer

from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1
watson_TTS = TextToSpeechV1(
            url='https://stream.watsonplatform.net/text-to-speech/api',
            username='xx',
            password='xx')

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
    #tmpFile = 'temp/temp_voice.wav' #Azure, HOYA
    tmpFile = 'temp/temp_voice.mp3' #Google, Watson
    if len(sys.argv)>=2:
        lng = sys.argv[1]
    if len(sys.argv)>=3:
        txtFile = sys.argv[2]
    if len(sys.argv)>=4:
        tmpFile = sys.argv[3]
    if lng=='ja':
        lng = 'ja-JP'

    print('')
    print('speech_output_watson.py')
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

    # Watson
    if lng=='ja-JP':
            vc='ja-JP_EmiVoice'
    else:
            vc='en-US_AllisonVoice'

    # Save
    audio=watson_TTS.synthesize(text=txt, accept='audio/mp3', voice=vc).get_result().content

    wb = open(tmpFile, 'wb')
    wb.write(audio)
    wb.close()
    wb = None

    try:
        print(' ' + txt)

    except:
        print(' Error!', sys.exc_info()[0])
        sys.exit()

    if os.path.exists(tmpFile):
        qPlay(tmpFile)



