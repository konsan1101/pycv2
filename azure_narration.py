#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import datetime
import time
import codecs
import cv2
from PIL import Image, ImageDraw, ImageFont

language = 'ja'



def v_output(txt):
    global language
    playFile='temp/temp_playSJIS.txt'

    if txt =='_ok':
        return txt

    #if txt !='_ok' and language == 'ja':
    #    txt = "<prosody rate='fast'>" + txt + "</prosody>"

    while os.path.exists(playFile):
        time.sleep(0.1)

    try:
        w = codecs.open(playFile, 'w', 'shift_jis')
        w.write(txt)
        w.close()
        w = None
    except:
        w = None
        try:
            w2 = open(playFile, 'w')
            w2.write(txt)
            w2.close()
            w2 = None
        except:
            w2 = None

    while os.path.exists(playFile):
        time.sleep(0.1)

    #print('v_output: ' + txt)

def v_micon():
    micON   ='temp/temp_micON.txt'
    print('v_micoff:microphone turn on')
    while not os.path.exists(micON):
        try:
            w = open(micON, 'w')
            w.write('ON')
            w.close()
            w = None
        except:
            w = None

def v_micoff():
    micON   ='temp/temp_micON.txt'
    print('v_micon_:microphone turn off')
    if os.path.exists(micON):
        try:
            os.remove(micON)
        except:
            pass

def v_input():
    recText1='temp/temp_recSJIS.txt'
    recText2='temp/temp_bakSJIS.txt'
    recTran1='temp/temp_recTranslator.txt'
    recTran2='temp/temp_bakTranslator.txt'

    if os.path.exists(recTran2):
            os.remove(recTran2)
    if os.path.exists(recText2):
            os.remove(recText2)
    if os.path.exists(recTran1):
            os.remove(recTran1)
    if os.path.exists(recText1):
            os.remove(recText1)

    v_micon()

    print('v_input_: wait')
    while not os.path.exists(recTran1):
        time.sleep(0.1)
    while not os.path.exists(recText1):
        time.sleep(0.1)

    v_micoff()

    os.rename(recTran1, recTran2)
    os.rename(recText1, recText2)

    txt = ''
    rt = codecs.open(recTran2, 'r', 'shift_jis')
    for t in rt:
        txt = (txt + ' ' + str(t)).strip()
    rt.close
    rt = None

    #print('v_input_: ' + txt)

    return str(txt)



def v_showinfo(imgf):

    if os.path.exists(imgf):
        load_img=cv2.imread(imgf)
        info_img = cv2.resize(load_img, (1250, 750))
        cv2.imshow('Info', info_img)
        cv2.moveWindow( 'Info', 0, 0)
        cv2.waitKey(1000)

def v_hideinfo():
    try:
        cv2.destroyWindow('Info')
    except:
        pass



if __name__ == '__main__':
    #global language
    print('narration:init')

    api      = 'azure'
    language = 'ja'
    miclevel = '0'
    micguide = 'off'
    filesjis = 'azure_narration_sjis.txt'
    if len(sys.argv)>=2:
        api      = sys.argv[1]
    if len(sys.argv)>=3:
        language = sys.argv[2]
    if len(sys.argv)>=4:
        miclevel = sys.argv[3]
    if len(sys.argv)>=5:
        filesjis = sys.argv[4]

    print('')
    print('narration:api     =' + str(api     ))
    print('narration:language=' + str(language))
    print('narration:miclevel=' + str(miclevel))
    print('narration:filesjis=' + str(filesjis))

    narration = []
    try:
        rt = codecs.open(filesjis, 'r', 'shift_jis')
        for s in rt:
            s = str(s).strip()
            if s != '':
                narration.append(s)
        rt.close
        rt = None
    except:
        pass

    v_micoff()

    p=subprocess.Popen(['python', '_speech_allinone.py', '0', 'usb', miclevel, micguide, api, language, language, 'ja', 'speech', 'temp/temp_micON.txt', 'temp/temp_recSJIS.txt'])

    print('')
    print('narration:start')

    v_output('_ok')
    v_output(u'ナレーション出力。開始。')
    time.sleep(1.5)

    for t in narration:
        v_output(str(t))
        time.sleep(1.5)

    v_output('_ok')
    v_output(u'ナレーション出力。終了。')
    time.sleep(1.5)

    print('')
    print('narration:terminate')

    time.sleep(60)
    v_hideinfo()
    p.terminate()

    print('narration:bye!')



