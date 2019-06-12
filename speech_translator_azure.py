#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import codecs

import requests
import xml.etree.ElementTree as ET

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
    print('speech_translator_azure.py')
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

    mstxt = ''
    try:
        print(' ' + txt)

        token = requests.post(
            'https://api.cognitive.microsoft.com/sts/v1.0/issueToken',
            headers = {
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': 'xx',
                }
            )
        res = requests.get(
            'https://api.microsofttranslator.com/v2/http.svc/Translate',
            headers = {
                'Content-Type': 'application/xml',
                },
            params={
                'appid': 'Bearer ' + token.text,
                'text': txt,
                'from': inplng,
                'to': outlng,
                'category': 'general',
                }
            )
        msxml = res.text
        mstxt = ET.fromstring(msxml).text

    except:
        print(' Error!', sys.exc_info()[0])
        sys.exit()

    print(' ' + mstxt)
    w = codecs.open(outFile, 'w', 'shift_jis')
    w.write(mstxt)
    w.close()
    w = None



