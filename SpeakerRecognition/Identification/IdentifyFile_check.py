#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import os
import time

import IdentificationServiceHttpClientHelper

import numpy as np
import cv2
import datetime
import glob
import codecs
import subprocess



def identify_file(stamp, profile_ids):
    subscription_key = 'xx'
    audio_path = '../temp/voices/' + str(stamp) + '_voice.wav'
    text_path  = '../temp/voices/' + str(stamp) + '_text_ja.txt'
    force_short_audio = 'True'

    id = ''
    cf = ''
    try:

        helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
            subscription_key)

        result = helper.identify_file(audio_path, profile_ids, force_short_audio.lower() == "true")

        id=result.get_identified_profile_id()
        cf=result.get_confidence()
        #print('Identified Speaker = {0}'.format(id))
        #print('Confidence = {0}'.format(cf))

    except:
        pass

    tx = ''
    try:
        r = codecs.open(text_path, "r", 'utf-8')
        for t in r:
            tx = (tx + ' ' + str(t)).strip()
        r.close
        r = None
    except:
        pass

    name   = ''
    img_url= ''
    if id != '':
        if id == '00000000-0000-0000-0000-000000000000':
            name = ""
        if id == '1713992c-7c55-466a-bbc8-051d0557b010':
            name = "azure"
        if id == '5310cdf7-a74c-4b47-b311-c97176b8502a':
            name = "google"
        if id == 'e6cd812d-e903-4856-99c6-f300159ba975':
            name = "hoya"
        if id == 'ad4260cc-9c5b-447e-aaf2-0042c83a15ea':
            name = "watson"
        if id == 'xx':
            name = "kondou"
            img_url = '../temp/kondou/20180131-181603_face.jpg'
        if id == 'xx':
            name = "yamanishi"
            img_url = '../temp/yamanishi/20180131-173138_face.jpg'
        if id == 'xx':
            name = "minabe"
            img_url = '../temp/minabe/20180201-183540_face.jpg'

    if name != '':
            print(stamp + ' ' + tx + ', ' + name + ', (' + cf + ')')
    else:
            print(stamp + ' ' + tx + ', ?????')

    if tx.find('おはよう') >= 0:
        if name != '' and img_url !='':
            print(stamp + ' Good morning ' + name + ',')
            try:
                w = codecs.open('../temp/temp_playSJIS.txt', 'w', 'shift_jis')
                w.write(name + u'さん。おはようございます。')
                w.close()
                w = None
            except:
                w = None

    if tx.find('行ってきます') >= 0:
        if name != '' and img_url !='':
            print(stamp + ' Be careful, Good luck, ' + name + ',')
            try:
                w = codecs.open('../temp/temp_playSJIS.txt', 'w', 'shift_jis')
                w.write(name + u'さん。お気をつけて、いってらっしゃい。')
                w.close()
                w = None
            except:
                w = None

    if tx.find('戻りました') >= 0:
        if name != '' and img_url !='':
            print(stamp + ' Welcome back, ' + name + ',')
            try:
                w = codecs.open('../temp/temp_playSJIS.txt', 'w', 'shift_jis')
                w.write(name + u'さん。お疲れさまでした。')
                w.close()
                w = None
            except:
                w = None

    if tx.find('お先に') >= 0:
        if name != '' and img_url !='':
            print(stamp + ' Good work, ' + name + ',')
            try:
                w = codecs.open('../temp/temp_playSJIS.txt', 'w', 'shift_jis')
                w.write(name + u'さん。お疲れさまでした。')
                w.close()
                w = None
            except:
                w = None

    if tx.find('バルス') >= 0:
        if name != '' and img_url !='':
            print(stamp + ' You say BARUSU ?, ' + name + ',')
            try:
                w = codecs.open('../temp/temp_playSJIS.txt', 'w', 'shift_jis')
                w.write(name + u'さん。機能停止の権限はありません。')
                w.close()
                w = None
            except:
                w = None

    if name != '':
            files = glob.glob("../temp/" + name + "/hit_*")
            for file in files:
                img_url = file

    if img_url != '':
            info_img=cv2.imread(img_url)
            cv2.putText(info_img, name, (20,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255))
            cv2.putText(info_img, cf  , (20,60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
            cv2.namedWindow("Infomation", 1)
            cv2.imshow(     "Infomation", info_img)
            sec=int(datetime.datetime.now().strftime('%S'))
            cv2.moveWindow( "Infomation", sec*10, 25)

            cv2.waitKey(10000)

            cv2.destroyWindow("Infomation")



if __name__ == '__main__':

    stamp = sys.argv[1]
    profile_ids=[
                 'xx'
                ,'xx'
                ,'xx'
                ,'xx'
                ,'xx'
                ,'xx'
                ,'xx'
                ]

    identify_file(stamp, profile_ids)



