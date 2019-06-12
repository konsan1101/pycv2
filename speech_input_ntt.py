#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import codecs

import requests



#http://rikoubou.hatenablog.com/entry/2017/09/11/231834



if __name__ == '__main__':



    APIKEY = 'xx'
    RECORD_FILE_PATH = '_sound_sample.wav'

    url = "https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize?APIKEY={}".format(APIKEY)
    files = {"a": open(RECORD_FILE_PATH, 'rb'), "v":"on"}
    r = requests.post(url, files=files)

    print(r.json()['text'])



