#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    inplng  = 'ja'
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
    if inplng=='ja-JP':
        inplng = 'ja'

    #pa = pyaudio.PyAudio()
    #for i in range(0, pa.get_host_api_count()):
    #    print(i, pa.get_host_api_info_by_index(i))

    print('')
    print('speech_input_google.py')
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

        if os.path.exists(recText):
            os.remove(recText)

        try:
            txt=srr.recognize_google(speech, language=inplng)

            print(' ' + txt)

            w = codecs.open(recText, 'w', 'shift_jis')
            w.write(txt)
            w.close()
            w = None

        except:
            print(' Error!', sys.exc_info()[0])
            sys.exit()



