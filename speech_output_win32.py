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

#https://stackoverflow.com/questions/49871252/saving-text-to-speech-python
import win32com.client as wincl
import win32api



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
    if lng=='en':
        lng = 'en-US'

    print('')
    print('speech_output_win32.py')
    print(' 1)language = ' + lng)
    print(' 2)txtFile  = ' + txtFile)
    #print(' 3)tmpFile  = ' + tmpFile)

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

        # MS Windows
        t  = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
        t += '<voice xml:lang="' + lng + '" gender="female">'
        t += txt
        t += '</voice></speak>'

        engine = wincl.Dispatch('SAPI.SpVoice')
        #engine.Speak(t)

        stream = wincl.Dispatch("SAPI.SpFileStream")
        stream.open(tmpFile, 3, False)
        #for speaker in engine.GetAudioOutputs():
        #    print(speaker.GetDescription())
        engine.AudioOutputStream = stream
        engine.Speak(t)
        stream.close()



    except:
        print(' Error!', sys.exc_info()[0])
        sys.exit()

    if os.path.exists(tmpFile):
        qPlay(tmpFile)



