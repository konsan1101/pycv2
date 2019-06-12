#!/usr/bin/env python
# -*- coding: utf-8 -*-

#http://blog.cgfm.jp/garyu/archives/3396
#xxx http://5st7.hatenablog.com/

import os
import sys
import datetime
import argparse
import subprocess
import requests
import pprint
 
 
#Docomo 音声合成 API
API_KEY = 'xx'
url = "https://api.apigw.smt.docomo.ne.jp/aiTalk/v1/textToSpeech?APIKEY="+API_KEY
 
 
#参考）音声合成 | docomo Developer support
#https://dev.smt.docomo.ne.jp/?p=docs.api.page&api_name=text_to_speech&p_name=api_1#tag01
#    'speaker' : "nozomi"、"seiji"、"akari"、"anzu"、"hiroshi"、"kaho"、"koutarou"、"maki"、"nanako"、"osamu"、"sumire"
#    'pitch' : ベースライン・ピッチ。 基準値:1.0、範囲:0.50～2.00
#    'range' : ピッチ・レンジ。基準値:1.0、範囲:0.00～2.00
#    'rate' : 読み上げる速度。基準値:1.0、範囲:0.50～4.00
#    'volume' : 音量。基準値:1.0、範囲:0.00～2.00
 
prm = {
    'speaker' : 'nozomi',
    'pitch' : '1',
    'range' : '1',
    'rate' : '1',
    'volume' : '1.5'
}
 
text = u'おはようございます'
 
 
# SSML生成
# ===========================================
xml = u'<?xml version="1.0" encoding="utf-8" ?>'
voice = '<voice name="' + prm["speaker"] + '">'
prosody = '<prosody rate="'+ prm['rate'] +'" pitch="'+ prm['pitch'] +'" range="'+ prm['range'] +'">'
xml += '<speak version="1.1">'+ voice + prosody + text + '</prosody></voice></speak>'
 
# utf-8にエンコード
xml = xml.encode("UTF-8")
 
 
# Docomo APIアクセス
# ===========================================
print("Start API")
 
response = requests.post(
    url,
    data=xml,
    headers={
        'Content-Type': 'application/ssml+xml',
        'Accept' : 'audio/L16',
        'Content-Length' : len(xml)
    }
)
 
#print(response)
#print(response.encoding)
#print(response.status_code)
#print(response.content)
 
if response.status_code != 200 :
    print("Error API : " + response.status_code)
    exit()
 
else :
    print("Success API")
 
#保存するファイル名
rawFile = "temp/temp_ntt.raw"
wavFile = "temp/temp_ntt.wav"
 
#バイナリデータを保存
fp = open(tmp + rawFile, 'wb')
fp.write(response.content)
fp.close()



# soxを使って raw→wavに変換
#cmd = "sox -t raw -r 16k -e signed -b 16 -B -c 1 " + rawFile + " "+ wavFile
cmd = "sox -t raw -r 16k -e signed -b 16 -B -c 1 " + rawFile + " -d "
# コマンドの実行
subprocess.check_output(cmd, shell=True)



