#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import codecs

import json
from watson_developer_cloud import LanguageTranslatorV3
watson_translator = LanguageTranslatorV3(
            version='2018-05-01',
            url='https://gateway.watsonplatform.net/language-translator/api',
            username='xx',
            password='xx')

if __name__ == '__main__':
    inplng  = 'ja'
    outlng  = 'en'
    inpFile = 'temp/temp_recText.txt'
    outFile = 'temp/temp_msg.txt'
    if len(sys.argv)>=2:
        inplng = sys.argv[1]
    if len(sys.argv)>=3:
        outlng = sys.argv[2]
    if len(sys.argv)>=4:
        inpFile = sys.argv[3]
    if len(sys.argv)>=5:
        outFile = sys.argv[4]
    if inplng=='ja-JP':
        inplng = 'ja'
    if outlng=='en-US':
        outlng = 'en'

    print('')
    print('speech_translator_watson.py')
    print(' 1)input  lang = ' + inplng)
    print(' 2)output lang = ' + outlng)
    print(' 3)input  file = ' + inpFile)
    print(' 4)output file = ' + outFile)

    txt = ''
    rt = codecs.open(inpFile, 'r', 'shift_jis')
    for t in rt:
        txt = (txt + ' ' + str(t)).strip()
    rt.close
    rt = None

    if os.path.exists(outFile):
        os.remove(outFile)

    outtxt=''
    try:
        print(' ' + txt)

        data = watson_translator.translate(
            text=txt,source=inplng,target=outlng
            ).get_result()

        #print(data)

        try:
            outtxt=data['translations'][0]['translation']
        except:
            pass

    except:
        print(' Error!', sys.exc_info()[0])
        sys.exit()

    print(' ' + outtxt)
    w = codecs.open(outFile, 'w', 'shift_jis')
    w.write(outtxt)
    w.close()
    w = None



