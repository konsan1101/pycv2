#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import cv2
import datetime
import time
import threading
import queue
import subprocess
import pygame
import codecs
import requests
import json

from PIL import Image, ImageDraw, ImageFont

print(os.path.dirname(__file__))
print(os.path.basename(__file__))
print(sys.version_info)
print(cv2.__version__)

FrameWidth = '?'
FrameHight = '?'
BaseEvent  = None
BaseX      = None
BaseY      = None

AZURE_CV_KEY = 'xx'

class fpsWithTick(object):
    def __init__(self):
        self._count     = 0
        self._oldCount  = 0
        self._freq      = 1000 / cv2.getTickFrequency()
        self._startTime = cv2.getTickCount()
    def get(self):
        nowTime         = cv2.getTickCount()
        diffTime        = (nowTime - self._startTime) * self._freq
        self._startTime = nowTime
        fps             = (self._count - self._oldCount) / (diffTime / 1000.0)
        self._oldCount  = self._count
        self._count     += 1
        fpsRounded      = round(fps, 2)
        return fpsRounded



def BaseMouseEvent(event, x, y, flags, param):
    global BaseEvent,BaseX,BaseY
    if event == cv2.EVENT_LBUTTONUP:
        BaseEvent = cv2.EVENT_LBUTTONUP
        BaseX     = x
        BaseY     = y
        #print('EVENT_LBUTTONUP')
    elif event == cv2.EVENT_RBUTTONDOWN:
        BaseEvent = cv2.EVENT_RBUTTONDOWN
        #print('EVENT_RBUTTONDOWN')



def qPlay(tempFile=None, sync=True):

        if not tempFile is None:
            #if os.name != 'nt':
            #    pygame.mixer.init()
            #    pygame.mixer.music.load(tempFile)
            #    pygame.mixer.music.play()
            #    if sync == True:
            #        while pygame.mixer.music.get_busy():
            #            time.sleep(0.3)
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
                #cmd = ['sox', tempFile, '-b', '8', '-u', '-r', '8000', '-c', '1', '-d', '-q']
                #cmd = ['sox', tempFile, '-r', '8000', '-c', '1', '-d', '-q']
                p=subprocess.Popen(cmd)
                if sync == True:
                    p.wait()



def sub_input(cn_r,cn_s):
    global FrameWidth,FrameHeight
    print('input___:init')

    camDev   = cn_r.get()
    camRotate= cn_r.get()
    camWidth = cn_r.get()
    camHeight= cn_r.get()
    camFps   = cn_r.get()
    imgWidth = cn_r.get()
    imgHeight= cn_r.get()
    cn_r.task_done()

    print('input___:device   =' + str(camDev   ))
    print('input___:camRotate=' + str(camRotate))
    print('input___:camWidth =' + str(camWidth ))
    print('input___:camHeight=' + str(camHeight))
    print('input___:camFps   =' + str(camFps   ))
    print('input___:imgWidth =' + str(imgWidth ))
    print('input___:imgHeight=' + str(imgHeight))

    capture = None
    if camdev.isdigit():
        capture = cv2.VideoCapture(int(camDev))
        capture.set(3, camWidth )
        capture.set(4, camHeight)
        capture.set(5, camFps   )
    else:
        capture = cv2.VideoCapture(camDev)

    print('input___:start')

    while True:
        if cn_r.qsize() > 0:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if mode_get is None:
                print('input___:None=break')
                break

            if cn_r.qsize() != 0 or cn_s.qsize() > 2:
                print('input___: queue overflow warning!',cn_r.qsize(),cn_s.qsize())

            if mode_get != 'RUN':
                cn_s.put(['PASS', ''])

            else:
                ret, frame = capture.read()

                if ret == False:
                    print('input___:capture error')
                    time.sleep(5.0)
                    cn_s.put(['END', ''])
                    break

                else:

                    # frame_img
                    FrameHeight, FrameWidth = frame.shape[:2]

                    #frame_hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    #frame_chan = cv2.split(frame_hsv)
                    #frame_chan[2] = cv2.equalizeHist(frame_chan[2])
                    #frame_hsv  = cv2.merge(frame_chan)
                    #frame_img  = cv2.cvtColor(frame_hsv, cv2.COLOR_HSV2BGR)
                    frame_img  = frame.copy()

                    # image_img
                    if abs(int(camRotate)) == 90:
                        frame_width2  = int((FrameWidth - FrameHeight)/2)
                        rect_img  = cv2.resize(frame_img[0:FrameHeight, frame_width2:FrameHeight], (960,960))
                        rect_mat  = cv2.getRotationMatrix2D((480, 480), int(rote), 1.0)
                        rect_r    = cv2.warpAffine(rect_img, rect_mat, (960, 960), flags=cv2.INTER_LINEAR)
                        image_img = cv2.resize(rect_r, (imgWidth, imgHeight))
                    elif abs(int(camRotate)) == 180:
                        image_img = cv2.resize(frame_img, (imgWidth, imgHeight))
                        image_img = cv2.flip(image_img,0) # 180 Rotation
                    else:
                        image_img = cv2.resize(frame_img, (imgWidth, imgHeight))

                    cn_s.put(['OK', image_img.copy()])

        if cn_r.qsize() == 0:
            time.sleep(0.05)

    print('input___:terminate')

    capture.release()

    print('input___:end')



def sub_compute(cn_r,cn_s):
    print('compute_:init')

    proc_width  = 480
    proc_height = 320

    casname1 = cn_r.get()
    casname2 = cn_r.get()
    extpgm   = cn_r.get()
    cn_r.task_done()

    if casname1 != 'None':
        casnm1=casname1[0:len(casname1)-4]
        print('compute_:' + str(casname1))
        cascade1 = cv2.CascadeClassifier(casname1)
        haar_scale1    = 1.1
        min_neighbors1 = 10
        min_size1      = ( 15, 15)
        if casname1 == 'cars.xml':
            haar_scale1    = 1.1
            min_neighbors1 = 3
            min_size1      = ( 15, 15)
    if casname2 != 'None':
        casnm2=casname2[0:len(casname2)-4]
        print('compute_:' + str(casname2))
        cascade2 = cv2.CascadeClassifier(casname2)
        haar_scale2    = 1.1
        min_neighbors2 = 15
        min_size2      = ( 20, 20)
        if casname1 == 'cars.xml':
            haar_scale2    = 1.1
            min_neighbors2 = 5
            min_size2      = ( 20, 20)
    if extpgm != 'None':
        print('compute_:extpgm=' + str(extpgm))

    last_hit=datetime.datetime.now()

    print('compute_:start')

    fps_class = fpsWithTick()
    while True:
        if cn_r.qsize() > 0:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if mode_get is None:
                print('compute_:None=break')
                break

            if cn_r.qsize() != 0 or cn_s.qsize() > 2:
                print('compute_: queue overflow warning!',cn_r.qsize(),cn_s.qsize())

            if mode_get != 'image':
                cn_s.put([ 0 , 0 ])

            else:
                image_img   = data_get.copy()
                image_height, image_width = image_img.shape[:2]
                proc_img    = image_img.copy()
                proc_height = int(proc_width * image_height / image_width)

                gray  = cv2.resize(image_img, (proc_width, proc_height))
                gray1 = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
                gray2 = cv2.equalizeHist(gray1)

                hit_count  = 0
                hit_count1 = 0
                hit_count2 = 0
                hit_img1   = None
                hit_img2   = None

                if casname1 != 'None':
                    rects1 = cascade1.detectMultiScale(gray2, scaleFactor=haar_scale1, minNeighbors=min_neighbors1, minSize=min_size1)
                    if rects1 is not None:
                        for (hit_x, hit_y, hit_w, hit_h) in rects1:
                            hit_count  += 1
                            hit_count1 += 1
                            x  = int(hit_x * image_width  / proc_width )
                            y  = int(hit_y * image_height / proc_height)
                            w  = int(hit_w * image_width  / proc_width )
                            h  = int(hit_h * image_height / proc_height)
                            if casname1 == 'face.xml':
                                if x>10:
                                    x -= 10
                                    w += 20
                                if y>10:
                                    y -= 10
                                    h += 20
                            if x<0:
                                 x=0
                            if y<0:
                                 y=0
                            if x+w>image_width:
                                 w=image_width-x
                            if y+h>image_height:
                                 h=image_height-y
                            cv2.rectangle(proc_img, (x,y), (x+w,y+h), (0,0,255), 2)

                            if hit_count1 == 1:
                                hit_img1 = cv2.resize(image_img[y:y+h, x:x+w],(h,w))

                if casname1 != 'None':
                    rects2 = cascade2.detectMultiScale(gray2, scaleFactor=haar_scale2, minNeighbors=min_neighbors2, minSize=min_size2)
                    if rects2 is not None:
                        for (hit_x, hit_y, hit_w, hit_h) in rects2:
                            hit_count  += 1
                            hit_count2 += 1
                            x  = int(hit_x * image_width  / proc_width )
                            y  = int(hit_y * image_height / proc_height)
                            w  = int(hit_w * image_width  / proc_width )
                            h  = int(hit_h * image_height / proc_height)
                            if x<0:
                                 x=0
                            if y<0:
                                 y=0
                            if x+w>image_width:
                                 w=image_width-x
                            if y+h>image_height:
                                 h=image_height-y
                            cv2.rectangle(proc_img, (x,y), (x+w,y+h), (0,255,0), 2)

                            if hit_count2 == 1:
                                hit_img2 = cv2.resize(image_img[y:y+h, x:x+w],(h,w))

                now=datetime.datetime.now()
                if hit_count1 > 0:
                    f1 = 'temp/images/' + now.strftime('%Y%m%d-%H%M%S') + '_' + casnm1 + '.jpg'
                    if not os.path.exists(f1):
                        cv2.imwrite(f1, hit_img1)
                        print('compute_:' + f1)

                    if now > last_hit + datetime.timedelta(seconds=5):
                        last_hit=now
                        if extpgm != 'None':
                            if os.path.exists(extpgm):
                                #os.system(extpgm + ' ' + f1)
                                p=subprocess.Popen([extpgm, f1])
                                #p.wait()

                if hit_count2 > 0:
                    f2 = 'temp/images/' + now.strftime('%Y%m%d-%H%M%S') + '_' + casnm2 + '.jpg'
                    if not os.path.exists(f2):
                        cv2.imwrite(f2, hit_img2)
                        print('compute_:' + f2)

                if (hit_count > 0):
                    fx = now.strftime('%Y%m%d-%H%M%S')
                    fx = fx[:14] + '0'
                    fx = 'temp/images/' + fx + '_photo.png'
                    if not os.path.exists(fx):
                        cv2.imwrite(fx, image_img)
                        print('compute_:' + fx)

                if hit_count > 0:
                    cn_s.put([hit_count, proc_img.copy()])
                else:
                    cn_s.put([ 0 , 0 ])

        if cn_r.qsize() == 0:
            time.sleep(0.5)

    print('compute_:end')



def sub_output(cn_r,cn_s):
    global FrameWidth,FrameHeight
    global BaseEvent,BaseX,BaseY
    print('output__:init')

    camRotate = cn_r.get()
    baseWidth = cn_r.get()
    baseHeight= cn_r.get()
    liveWidth = cn_r.get()
    liveHeight= cn_r.get()
    cn_r.task_done()

    print('output__:camRotate =' + str(camRotate ))
    print('output__:baseWidth =' + str(baseWidth ))
    print('output__:baseHeight=' + str(baseHeight))
    print('output__:liveWidth =' + str(liveWidth ))
    print('output__:liveHeight=' + str(liveHeight))

    blue_img = np.zeros((240,320,3), np.uint8)
    cv2.rectangle(blue_img,(0,0),(320,240),(255,0,0),-1)
    cv2.putText(blue_img, 'No Data !', (40,80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
    white_img = np.zeros((240,320,3), np.uint8)
    cv2.rectangle(white_img,(0,0),(320,240),(255,255,255),-1)
    image_img    = cv2.resize(blue_img, (baseWidth, baseHeight ))
    base_img     = cv2.resize(blue_img, (baseWidth, baseHeight ))
    live_img     = cv2.resize(blue_img, (liveWidth, liveHeight))
    compute_img  = base_img.copy()
    compute_beat = 0
    capture_img  = None
    text_beat    = 0
    text_text    = ''
    text_img     = None
    tran_beat    = 0
    tran_text    = ''
    tran_img     = None
    testcv_beat  = 0
    testcv_img   = None

    frame_src    = '?'
    frame_fps    = '?'

    cv2.namedWindow('Base',  1)
    cv2.imshow(     'Base',  base_img)
    cv2.moveWindow( 'Base',  -15,   -55)
    cv2.setMouseCallback('Base', BaseMouseEvent)

    print('output__:start')

    fps_class = fpsWithTick()
    while True:
        if cn_r.qsize() > 0:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if mode_get is None:
                print('output__:None=break')
                break

            if cn_r.qsize() != 0 or cn_s.qsize() > 2:
                print('output__: queue overflow warning!',cn_r.qsize(),cn_s.qsize())

            if mode_get == 'image':
                image_img    = data_get.copy()
                image_height, image_width = image_img.shape[:2]
                frame_src = str(FrameWidth) + 'x' + str(FrameHeight)
                frame_fps = str(fps_class.get())

            if mode_get == 'compute':
                compute_img  = data_get.copy()
                compute_beat = time.time()
                if abs(int(camRotate)) == 360:
                    compute_img = cv2.flip(compute_img,1) # Mirror image

            if mode_get == 'speech_text':
                if data_get != '':
                    text_text  = str(data_get)
                    text_beat  = time.time()

                    # 文字列を描画する
                    font = ImageFont.truetype('_font_meiryob.ttc', 25, encoding='unic')
                    text_draw = Image.new('RGB', (int(baseWidth/2),50), (0xff, 0xff, 0xff))
                    draw = ImageDraw.Draw(text_draw)
                    draw.text((10, 10), text_text, font=font, fill=(0x00, 0x00, 0x00))
                    #text_draw.save('temp/temp_capture_text.jpg')
                    #text_img=cv2.imread('temp/temp_capture_text.jpg')
                    text_img=np.asarray(text_draw)

            if mode_get == 'speech_tran':
                if data_get != '':
                    tran_text  = str(data_get)
                    tran_beat  = time.time()

                    # 文字列を描画する
                    font = ImageFont.truetype('_font_meiryob.ttc', 25, encoding='unic')
                    tran_draw = Image.new('RGB', (int(baseWidth/2),50), (0xff, 0xff, 0xff))
                    draw = ImageDraw.Draw(tran_draw)
                    draw.text((10, 10), tran_text, font=font, fill=(0x00, 0x00, 0x00))
                    #tran_draw.save('temp/temp_capture_tran.jpg')
                    #tran_img=cv2.imread('temp/temp_capture_tran.jpg')
                    tran_img=np.asarray(tran_draw)

            if mode_get == 'testcv':
                testcv_img   = data_get.copy()
                testcv_height, testcv_width = testcv_img.shape[:2]
                testcv_beat  = time.time()

            # base_img
            base_img = cv2.resize(image_img, (baseWidth, baseHeight))
            if abs(int(camRotate)) == 360:
                base_img = cv2.flip(base_img,1) # Mirror image
            cv2.putText(base_img, frame_src, (40,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255))
            cv2.putText(base_img, frame_fps, (40,70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))

            # live_img
            live_img = cv2.resize(image_img, (liveWidth, liveHeight))
            if abs(int(camRotate)) == 360:
                live_img = cv2.flip(live_img,1) # Mirror image
            cv2.putText(live_img, frame_src, (40,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255))
            cv2.putText(live_img, frame_fps, (40,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))

            # compute_img
            sec = int(time.time() - compute_beat)
            if sec < 5:
                base_img = cv2.resize(compute_img, (baseWidth, baseHeight))
                base_img[25:liveHeight+25, baseWidth-liveWidth-25:baseWidth-25] = live_img.copy()
                cv2.rectangle(base_img, (baseWidth-liveWidth-25,25), (baseWidth-25,liveHeight+25), (255,255,255), 1)
                if int(time.time()) % 2 == 1:
                    cv2.rectangle(base_img, (10,10), (baseWidth-10,baseHeight-10), (255,255,255), 20)
                else:
                    cv2.rectangle(base_img, (10,10), (baseWidth-10,baseHeight-10), (0,0,255), 20)

            # base_img
            cv2.putText(base_img, 'CANCEL', (40,baseHeight-100), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,255))
            cv2.rectangle(base_img,(35,baseHeight-95),(300,baseHeight-150),(0,0,255),2)
            cv2.putText(base_img, 'ENTER', (baseWidth-300,baseHeight-100), cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255))
            cv2.rectangle(base_img,(baseWidth-305,baseHeight-95),(baseWidth-75,baseHeight-150),(255,255,255),2)

            # text alpha blending
            sec = int(time.time() - text_beat)
            if sec < 60:
                try:
                    src_img=base_img[100:100+50, 50:50+int(base_width/2)]
                    alpha_img= cv2.addWeighted(src_img, 0.6, text_img, 0.4, 0.0)
                    base_img[100:100+50, 50:50+int(base_width/2)] = alpha_img
                except:
                    print('output__:text alpha blending error!')
                    text_beat = 0

            # tran alpha blending
            sec = int(time.time() - tran_beat)
            if sec < 60:
                try:
                    src_img=base_img[160:160+50, 50:50+int(base_width/2)]
                    alpha_img= cv2.addWeighted(src_img, 0.6, tran_img, 0.4, 0.0)
                    base_img[160:160+50, 50:50+int(base_width/2)] = alpha_img
                except:
                    print('output__:tran alpha blending error!')
                    tran_beat = 0

            # testcv alpha blending
            sec = int(time.time() - testcv_beat)
            if sec < 10:
                try:
                    src_img=base_img[250:250+testcv_height, 50:50+testcv_width]
                    alpha_img= cv2.addWeighted(src_img, 0.6, testcv_img, 0.4, 0.0)
                    base_img[250:250+testcv_height, 50:50+testcv_width] = alpha_img
                except:
                    print('output__:testcv result alpha blending error!')
                    testcv_beat = 0

            cv2.imshow('Base', base_img )
            cv2.moveWindow( 'Base',  -15,   -55)
            cv2.setMouseCallback('Base', BaseMouseEvent)

            if cv2.waitKey(10) >= 0:
                print('output__:KEYS')
                cn_s.put(['KEYPRESS', ''])
                break

            if BaseEvent == cv2.EVENT_RBUTTONDOWN:
                BaseEvent = None
                print('output__:R-CLICK')
                cn_s.put(['R-CLICK', ''])
                break

            if BaseEvent == cv2.EVENT_LBUTTONUP:
                BaseEvent = None

                # ENTER,CANCEL
                if ((not BaseX is None) and (not BaseY is None)):
                    mode_get = 'shutter'
                    if (BaseY >= base_height-150 and BaseY <= base_height):
                        if (BaseX >= 0 and BaseX <= 350):
                            mode_get = 'cancel'
                        elif (BaseX >= base_width - 350 and BaseX <= base_width):
                            mode_get = 'enter'

            if mode_get == 'cancel':
                print('output__:CANCEL')
                ft = 'temp/temp_camResult.txt'
                wt = codecs.open(ft, 'w', 'utf-8')
                wt.write('CANCEL')
                wt.close()
                wt = None
                cn_s.put(['CANCEL', ''])
                break

            if mode_get == 'enter':
                print('output__:ENTER')
                ft = 'temp/temp_camResult.txt'
                wt = codecs.open(ft, 'w', 'utf-8')
                wt.write('ENTER')
                wt.close()
                wt = None
                cn_s.put(['ENTER', ''])
                break

            if mode_get == 'shutter':
                #cap_img  = image_img
                #white_img=cv2.resize(white_img, (image_width, image_height))
                cap_img  = base_img
                white_img=cv2.resize(white_img, (baseWidth, baseHeight))

                alpha_img= cv2.addWeighted(cap_img, 0.5, white_img, 0.5, 0.0)
                cv2.imshow('Base', alpha_img )

                if cv2.waitKey(10) >= 0:
                    print('output__:KEYS')
                    cn_s.put(['KEYPRESS', ''])
                    break

                # Shutter
                qPlay('_shutter')

                # Image Save
                now=datetime.datetime.now()
                fx = 'temp/capture/' + now.strftime('%Y%m%d-%H%M%S') + '_image.jpg'
                cv2.imwrite(fx, cap_img)
                print('output__:' + fx)
                fy = 'temp/temp_camCapture.jpg'
                cv2.imwrite(fy, cap_img)
                #print('output__:' + fy)

                speech_txt  = ''
                speech_beat = 0
                speech_img  = None

                # 90 Rotate & Gray save
                #rect_img = np.zeros((image_width, image_width,3), np.uint8)
                #rect_img[0:image_height, 0:image_width] = image_img.copy()
                #rect_mat = cv2.getRotationMatrix2D((int(image_width/2), int(image_width/2)), int(-90), 1.0)
                #rect_r   = cv2.warpAffine(rect_img, rect_mat, (image_width, image_width), flags=cv2.INTER_LINEAR)
                #rect_img2 = np.zeros((image_width,image_height,3), np.uint8)
                #cv2.rectangle(rect_img2,(0,0),(image_height,image_width),(255,255,255),-1)
                #rect_img2[1:image_width-1, 1:image_height-1] = rect_r[1:image_width-1, image_width-image_height+1:image_width-1]
                #rect_gray = cv2.cvtColor(rect_img2, cv2.COLOR_BGR2GRAY)
                #cv2.imwrite(fx, rect_gray)
                #print('output__:' + fx)

            if capture_img is None:
                cn_s.put(['OK', ''])
            else:
                cn_s.put(['capture', capture_img])
                capture_img = None

        if cn_r.qsize() == 0:
            time.sleep(0.05)

    print('output__:terminate')

    cv2.destroyAllWindows()

    print('output__:end')



def sub_speech(cn_r,cn_s):
    print('speech__:init')

    print('speech__:start')

    while True:
        if cn_r.qsize() > 0:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if mode_get is None:
                print('speech__:None=break')
                break

            if cn_r.qsize() != 0 or cn_s.qsize() > 2:
                print('speech__: queue overflow warning!',cn_r.qsize(),cn_s.qsize())

            if mode_get != 'RUN':
                cn_s.put(['PASS', ''])
            else:

                recText1='temp/temp_recSJIS.txt'
                recText2='temp/temp_bakSJIS.txt'
                recWave1='temp/temp_recWave.wav'
                recWave2='temp/temp_bakWave.wav'
                recTran1='temp/temp_recTranslator.txt'
                recTran2='temp/temp_bakTranslator.txt'

                if os.path.exists(recText1):
                    if os.path.exists(recText2):
                        try:
                            os.remove(recText2)
                        except:
                            pass
                if os.path.exists(recWave1):
                    if os.path.exists(recWave2):
                        try:
                            os.remove(recWave2)
                        except:
                            pass
                if os.path.exists(recTran1):
                    if os.path.exists(recTran2):
                        try:
                            os.remove(recTran2)
                        except:
                            pass

                hit_text = ''
                hit_tran = ''

                if os.path.exists(recText1):
                    if not os.path.exists(recText2):

                        now=datetime.datetime.now()
                        ft = 'temp/capture/' + now.strftime('%Y%m%d-%H%M%S') + '_sjis.txt'
                        fw = 'temp/capture/' + now.strftime('%Y%m%d-%H%M%S') + '_wave.wav'

                        if os.path.exists(recWave1):
                            if not os.path.exists(recWave2):
                                try:
                                    os.rename(recWave1, recWave2)
                                    rb = open(recWave2, 'rb')
                                    wav=rb.read()
                                    rb.close
                                    rb = None
                                    wb = open(fw, 'wb')
                                    wb.write(wav)
                                    wb.close
                                    wb = None
                                except:
                                    rb = None
                                    wb = None

                        if os.path.exists(recTran1):
                            if not os.path.exists(recTran2):
                                try:
                                    os.rename(recTran1, recTran2)
                                    txt = ''
                                    rt = codecs.open(recTran2, 'r', 'utf-8')
                                    for t in rt:
                                        txt = (txt + ' ' + str(t)).strip()
                                    rt.close
                                    rt = None

                                    hit_tran = txt
                                except:
                                    rt = None

                        try:
                                    os.rename(recText1, recText2)
                                    txt = ''
                                    rt = codecs.open(recText2, 'r', 'shift_jis')
                                    for t in rt:
                                        txt = (txt + ' ' + str(t)).strip()
                                    rt.close
                                    rt = None

                                    hit_text = txt

                                    wt = codecs.open(ft, 'w', 'shift_jis')
                                    wt.write(txt)
                                    wt.close()
                                    wt = None
                        except:
                                    rt = None
                                    wt = None

                if hit_text != '':
                    if hit_tran.lower() == 'shutter':
                        cn_s.put(['text', 'shutter'])
                    elif hit_tran.lower() == 'shooting':
                        cn_s.put(['text', 'shutter'])
                    elif hit_tran.lower() == 'photo':
                        cn_s.put(['text', 'shutter'])
                    elif hit_tran.lower() == 'enter':
                        cn_s.put(['text', 'enter'])
                    elif hit_tran.lower() == 'cancel':
                        cn_s.put(['text', 'cancel'])
                    else:
                        cn_s.put(['text', hit_text])
                        if hit_tran != '':
                            cn_s.put(['tran', hit_tran])
                else:
                    cn_s.put(['NG', ''])

        if cn_r.qsize() == 0:
            time.sleep(1.0)

    print('speech__:terminate')

    print('speech__:end')



def sub_testcv(cn_r,cn_s):
    global AZURE_CV_KEY
    print('testcv__:init')

    baseWidth = cn_r.get()
    baseHeight= cn_r.get()
    cn_r.task_done()

    print('testcv__:baseWidth =' + str(baseWidth ))
    print('testcv__:baseHeight=' + str(baseHeight))

    procWidth = 640
    drawWidth = int(baseWidth/2)
    lng = 'ja'

    print('testcv__:start')

    while True:
        if cn_r.qsize() > 0:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()

            if mode_get is None:
                print('testcode:None=break')
                break

            if cn_r.qsize() != 0 or cn_s.qsize() > 2:
                print('testcv__: queue overflow warning!',cn_r.qsize(),cn_s.qsize())

            if mode_get != 'image' and mode_get != 'capture':
                cn_s.put(['PASS', ''])

            else:
                image_img = data_get.copy()

                res_text = []
                res_text.append('Computer Vision Results.')

                if 1==1:
                #try:
                    if len(image_img.shape) == 3:
                        image_height, image_width, image_channels = image_img.shape[:3]
                    else:
                        image_height, image_width = image_img.shape[:2]
                        image_channels = 1

                    file_color = 'temp/temp_testcv_color.jpg'
                    file_gray  = 'temp/temp_testcv_gray.jpg'

                    procHeight = int(procWidth * image_height / image_width)
                    procImage  = cv2.resize(image_img, (procWidth, procHeight))

                    cv2.imwrite(file_color, procImage)

                    if image_channels != 1:
                        gray_img = cv2.cvtColor(procImage, cv2.COLOR_BGR2GRAY)
                    else:
                        gray_img = procImage.copy()

                    # ヒスト補正
                    hist_img = cv2.equalizeHist(gray_img)
                    # ぼやかし
                    #blur_img = cv2.blur(gray_img, (3,3), 0)
                    # 2値化
                    #_, thresh_img = cv2.threshold(gray_img, 140, 255, cv2.THRESH_BINARY)

                    #cv2.imwrite(file_gray, gray_img)
                    cv2.imwrite(file_gray, hist_img)

                #except:
                #    pass

                # CV
                #try:
                if 1==1:

                    #color_image=cv2.imread(file_color)
                    #cv2.imshow('Color', color_image)
                    #cv2.waitKey(5000)
                    #cv2.destroyWindow('Color')

                    img_color = open(file_color, 'rb')
                    res = requests.post('https://eastasia.api.cognitive.microsoft.com/vision/v1.0/analyze',
                          headers = {'Content-Type': 'application/octet-stream',
                          'Ocp-Apim-Subscription-Key': AZURE_CV_KEY,},
                          params = {'visualFeatures': 'Categories,Description',
                                    'language': 'en',},
                          data = img_color)
                    js = json.loads(res.text)

                    res_text.append('')
                    res_text.append('[ categories ]')
                    s  = ''
                    for names in js.get('categories'):
                        s  += str(names.get('name')).replace('_',' ') + ', '
                        if len(s) > int(drawWidth/11):
                            res_text.append('  ' + s)
                            s = ''
                    if s != '':
                        res_text.append('  ' + s)

                    res_text.append('')
                    res_text.append('[ captions ]')
                    s  = ''
                    for texts in js.get('description').get('captions'):
                        s  = str(texts.get('text'))
                        if len(s) > int(drawWidth/11):
                            res_text.append('  ' + s)
                            s = ''
                    if s != '':
                        res_text.append('  ' + s)

                    res_text.append('')
                    res_text.append('[ description ]')
                    s  = ''
                    for tag in js.get('description').get('tags'):
                        s  += str(tag) + ', '
                        if len(s) > int(drawWidth/11):
                            res_text.append('  ' + s)
                            s = ''
                    if s != '':
                        res_text.append('  ' + s)

                # OCR
                #try:
                if 1==1:

                    #gray_image=cv2.imread(file_gray)
                    #cv2.imshow('Gray', gray_image)
                    #cv2.waitKey(5000)
                    #cv2.destroyWindow('Gray')

                    img_gray = open(file_gray, 'rb')
                    res = requests.post('https://eastasia.api.cognitive.microsoft.com/vision/v1.0/ocr',
                          headers = {'Content-Type': 'application/octet-stream',
                          'Ocp-Apim-Subscription-Key': AZURE_CV_KEY,},
                          params = {'detectOrientation': 'true',
                                    'language': lng,},
                          data = img_gray)
                    js = json.loads(res.text)

                    res_text.append('')
                    res_text.append('[ OCR ]')
                    for region in js.get('regions'):
                        for line in region.get('lines'):
                            s = ''
                            for word in line.get('words'):
                                s += word.get('text')
                            res_text.append(s)
                    res_text.append('')

                #except:
                #    pass

                # 文字列出力
                if mode_get == 'capture':
                    now=datetime.datetime.now()
                    stamp=now.strftime('%Y%m%d-%H%M%S')
                    recText = 'temp/capture/' + stamp + '_cvSJIS.txt'
                    w = codecs.open(recText, 'w', 'shift_jis')
                    for i in range(0, len(res_text)):
                        w.write(res_text[i] + '\r\n')
                    w.close()
                    w = None

                # 文字列を描画する
                if baseWidth <= 1024:
                    font12 = ImageFont.truetype('_font_meiryob.ttc', 12, encoding='unic')
                    text_img = Image.new('RGB', (drawWidth,10+20*len(res_text)), (0xff, 0xff, 0xff))
                    text_draw = ImageDraw.Draw(text_img)
                    for i in range(0, len(res_text)):
                        text_draw.text((5, 5+20*i), res_text[i], font=font12, fill=(0x00, 0x00, 0x00))
                    #text_img.save('temp/temp_testcv_text.jpg')
                    #res_image=cv2.imread('temp/temp_testcv_text.jpg')
                    res_image=np.asarray(text_img)
                else:
                    font18 = ImageFont.truetype('_font_meiryob.ttc', 18, encoding='unic')
                    text_img = Image.new('RGB', (drawWidth,10+30*len(res_text)), (0xff, 0xff, 0xff))
                    text_draw = ImageDraw.Draw(text_img)
                    for i in range(0, len(res_text)):
                        text_draw.text((5, 5+30*i), res_text[i], font=font18, fill=(0x00, 0x00, 0x00))
                    #text_img.save('temp/temp_testcv_text.jpg')
                    #res_image=cv2.imread('temp/temp_testcv_text.jpg')
                    res_image=np.asarray(text_img)

                cn_s.put(['OK', res_image.copy()])
                image_img = None

        if cn_r.qsize() == 0:
            time.sleep(1.0)

    print('testcv__:terminate')

    print('testcv__:end')



if __name__ == '__main__':
    print('__main__:init')
    print('__main__:exsample.py device, rotate, cascade1, cascade2, extprogram, testsec,')

    camResult ='temp/temp_camResult.txt'
    camCapture='temp/temp_camCapture.jpg'
    if os.path.exists(camResult):
        os.remove(camResult)
    if os.path.exists(camCapture):
        os.remove(camCapture)

    camdev  = '0'
    rote    =   0  #normal
    #rote   =  90  #left
    #rote   = -90  #right
    #rote   = 180  #back
    #rote   = 360  #Mirror
    camres  = 640
    cas1    = 'face.xml'
    cas2    = 'fullbody.xml'
    extpgm  = 'None'
    testsec = '0'

    if len(sys.argv)>=2:
        camdev  = sys.argv[1]
    if len(sys.argv)>=3:
        rote    = sys.argv[2]
    if len(sys.argv)>=4:
        camres  = sys.argv[3]
    if len(sys.argv)>=5:
        cas1    = sys.argv[4]
    if len(sys.argv)>=6:
        cas2    = sys.argv[5]
    if len(sys.argv)>=7:
        extpgm  = sys.argv[6]
    if len(sys.argv)>=8:
        testsec = sys.argv[7]

    print('')
    print('__main__:device  =' + str(camdev ))
    print('__main__:rotate  =' + str(rote   ))
    print('__main__:camres  =' + str(camres ))
    print('__main__:cascade1=' + str(cas1   ))
    print('__main__:cascade2=' + str(cas2   ))
    print('__main__:program =' + str(extpgm ))
    print('__main__:testing =' + str(testsec))

    cam_width    = int(camres)
    if int(camres) != 1920:
        cam_height   = 480
        cam_fps      = 15
    else:
        cam_height   = 1080
        cam_fps      = 15

    if int(camres) <= 1024:
        image_width  = 640
        image_height = int(image_width * cam_height / cam_width)
    else:
        image_width  = 960
        image_height = int(image_width * cam_height / cam_width)

    if int(camres) != 1920:
        base_width   = 1024
        base_height  = int(base_width * cam_height / cam_width)
    else:
        base_width   = 1920
        base_height  = int(base_width * cam_height / cam_width)

    live_width   = int(base_width / 3)
    live_height  = int(live_width * cam_height / cam_width)

    print('')
    print('__main__:start')
    main_start   = time.time()

    output_s     = queue.Queue()
    output_r     = queue.Queue()
    output_proc  = None
    output_beat  = 0
    capture_img  = None
    compute_s    = queue.Queue()
    compute_r    = queue.Queue()
    compute_proc = None
    compute_beat = 0
    compute_img  = None
    input_s      = queue.Queue()
    input_r      = queue.Queue()
    input_proc   = None
    input_beat   = 0
    input_img1   = None
    input_img2   = None
    speech_s     = queue.Queue()
    speech_r     = queue.Queue()
    speech_proc  = None
    speech_beat  = 0
    speech_text  = ''
    speech_tran  = ''
    testcv_s     = queue.Queue()
    testcv_r     = queue.Queue()
    testcv_proc  = None
    testcv_beat  = 0
    testcv_last  = 0
    testcv_img   = None
    while True:

        # Thread timeout check

        if (input_r.qsize() == 0) and (input_beat != 0):
            sec = int(time.time() - input_beat)
            if sec > 60:
                print('__main__:input_proc 60s')
                #input_beat = time.time()
                print('__main__:input_proc break')
                input_s.put([None, None])
                time.sleep(3.0)
                input_proc = None
                input_beat = 0
                input_img1 = None
                input_img2 = None

        if (compute_r.qsize() == 0) and (compute_beat != 0):
            sec = int(time.time() - compute_beat)
            if sec > 60:
                print('__main__:compute_proc 60s')
                #compute_beat = time.time()
                print('__main__:compute_proc break')
                compute_s.put([None, None])
                time.sleep(3.0)
                compute_proc = None
                compute_beat = 0
                compute_img  = None

        if (output_r.qsize() == 0) and (output_beat != 0):
            sec = int(time.time() - output_beat)
            if sec > 60:
                print('__main__:output_proc 60s')
                #output_beat = time.time()
                print('__main__:output_proc break')
                output_s.put([None, None])
                time.sleep(3.0)
                output_proc = None
                output_beat = 0
                capture_img = None

        if (speech_r.qsize() == 0) and (speech_beat != 0):
            sec = int(time.time() - speech_beat)
            if sec > 60:
                print('__main__:speech_proc 60s')
                #speech_beat = time.time()
                print('__main__:speech_proc break')
                speech_s.put([None, None])
                time.sleep(3.0)
                speech_proc = None
                speech_beat = 0
                speech_text = ''
                speech_tran = ''

        if (testcv_r.qsize() == 0) and (testcv_beat != 0):
            sec = int(time.time() - testcv_beat)
            if sec > 60:
                print('__main__:testcv_proc 60s')
                #testcv_beat = time.time()
                print('__main__:testcv_proc break')
                testcv_s.put([None, None])
                time.sleep(3.0)
                testcv_proc = None
                testcv_beat = 0
                testcv_last = 0
                testcv_img  = None

        # Thread start

        if output_proc is None:
            while output_s.qsize() > 0:
                dummy = output_s.get()
            while output_r.qsize() > 0:
                dummy = output_r.get()
            output_proc = threading.Thread(target=sub_output, args=(output_s,output_r,))
            output_proc.daemon = True
            output_s.put(rote)
            output_s.put(base_width)
            output_s.put(base_height)
            output_s.put(live_width)
            output_s.put(live_height)
            output_proc.start()
            time.sleep(1.0)

            output_s.put(['START', ''])
            output_beat = time.time()

        if compute_proc is None:
            while compute_s.qsize() > 0:
                dummy = compute_s.get()
            while compute_r.qsize() > 0:
                dummy = compute_r.get()
            compute_proc = threading.Thread(target=sub_compute, args=(compute_s, compute_r,))
            compute_proc.daemon = True
            compute_s.put(cas1)
            compute_s.put(cas2)
            compute_s.put(extpgm)
            compute_proc.start()
            time.sleep(1.0)

            compute_s.put(['START', ''])
            compute_beat = time.time()

        if input_proc is None:
            while input_s.qsize() > 0:
                dummy = input_s.get()
            while input_r.qsize() > 0:
                dummy = input_r.get()
            input_proc = threading.Thread(target=sub_input, args=(input_s,input_r,))
            input_proc.daemon = True
            input_s.put(camdev)
            input_s.put(rote)
            input_s.put(cam_width)
            input_s.put(cam_height)
            input_s.put(cam_fps)
            input_s.put(image_width)
            input_s.put(image_height)
            input_proc.start()
            time.sleep(1.0)

            input_s.put(['START', ''])
            input_beat = time.time()

        if speech_proc is None:
            while speech_s.qsize() > 0:
                dummy = speech_s.get()
            while speech_r.qsize() > 0:
                dummy = cpeech_r.get()
            speech_proc = threading.Thread(target=sub_speech, args=(speech_s, speech_r,))
            speech_proc.daemon = True
            speech_proc.start()
            time.sleep(1.0)

            speech_s.put(['START', ''])
            speech_beat = time.time()

        if testcv_proc is None:
            while testcv_s.qsize() > 0:
                dummy = testcv_s.get()
            while testcv_r.qsize() > 0:
                dummy = testcv_r.get()
            testcv_proc = threading.Thread(target=sub_testcv, args=(testcv_s, testcv_r,))
            testcv_proc.daemon = True
            testcv_s.put(base_width)
            testcv_s.put(base_height)
            testcv_proc.start()
            time.sleep(1.0)

            testcv_s.put(['START', ''])
            testcv_beat = time.time()

        # processing

        if speech_r.qsize() > 0:
            speech_get = speech_r.get()
            speech_res = speech_get[0]
            speech_dat = speech_get[1]
            speech_r.task_done()
            if speech_res == 'text':
                speech_t = speech_dat
                if speech_t != '':
                    speech_text = speech_t
            if speech_res == 'tran':
                speech_t = speech_dat
                if speech_t != '':
                    speech_tran = speech_t
        if speech_r.qsize() == 0 and speech_s.qsize() == 0:
            speech_s.put(['RUN', ''])
            speech_beat = time.time()

        if input_r.qsize() > 0:
            input_get = input_r.get()
            input_res = input_get[0]
            input_dat = input_get[1]
            input_r.task_done()
            input_s.put(['RUN', ''])
            input_beat = time.time()
            if input_res == 'END':
                break
            if input_res == 'OK':
                input_img1 = input_dat.copy()
                input_img2 = input_dat.copy()

        if compute_r.qsize() > 0 and not input_img2 is None:
            compute_get = compute_r.get()
            compute_res = compute_get[0]
            compute_dat = compute_get[1]
            compute_r.task_done()
            compute_s.put(['image', input_img2.copy()])
            compute_beat = time.time()
            if int(compute_res) != 0:
                compute_img = compute_dat.copy()

        output_res = 'NG'
        if output_r.qsize() > 0:
            output_get = output_r.get()
            output_res = output_get[0]
            output_dat = output_get[1]
            output_r.task_done()
            if output_res == 'capture':
                capture_img = output_dat.copy()
            if output_res == 'CANCEL':
                break
            if output_res == 'ENTER':
                break
            if output_res == 'KEYPRESS':
                break
            if output_res == 'R-CLICK':
                break

        if output_res != 'NG':
            if speech_text != '':
                if speech_text == 'shutter':
                    output_s.put(['shutter', ''])
                    output_beat = time.time()
                    speech_text = ''
                    output_res = 'NG'
                elif speech_text == 'enter':
                    output_s.put(['enter', ''])
                    output_beat = time.time()
                    speech_text = ''
                    output_res = 'NG'
                elif speech_text == 'cancel':
                    output_s.put(['cancel', ''])
                    output_beat = time.time()
                    speech_text = ''
                    output_res = 'NG'
                else:
                    output_s.put(['speech_text', speech_text])
                    output_beat = time.time()
                    speech_text = ''
                    output_res = 'NG'

        if output_res != 'NG':
            if speech_tran != '':
                output_s.put(['speech_tran', speech_tran])
                output_beat = time.time()
                speech_tran = ''
                output_res = 'NG'

        if output_res != 'NG':
            if not testcv_img is None:
                output_s.put(['testcv', testcv_img.copy()])
                output_beat = time.time()
                testcv_img = None
                output_res = 'NG'

        if output_res != 'NG':
            if not compute_img is None:
                output_s.put(['compute', compute_img.copy()])
                output_beat = time.time()
                compute_img = None
                output_res = 'NG'

        if output_res != 'NG':
            if not input_img1 is None:
                output_s.put(['image', input_img1.copy()])
                output_beat = time.time()
                input_img1 = None
            else:
                output_s.put(['PASS', ''])
                output_beat = time.time()

        if testcv_r.qsize() > 0 and not input_img2 is None:
            testcv_get = testcv_r.get()
            testcv_res = testcv_get[0]
            testcv_dat = testcv_get[1]
            testcv_r.task_done()
            if testcv_res == 'OK':
                testcv_img = testcv_dat.copy()

            if int(testsec) == 0:
                testcv_s.put(['PASS', ''])
                testcv_beat = time.time()
            else:
                testflag=False
                if not capture_img is None:
                    testflag = True
                    testcv_s.put(['capture', capture_img.copy()])
                    testcv_beat = time.time()
                    testcv_last = time.time()
                    capture_img = None
                else:
                    sec1 = int(time.time() - main_start)
                    sec2 = int(time.time() - testcv_last)
                    if sec1 <= int(testsec) and sec2 >= 30:
                        testflag = True
                    if sec2 >= 3600:
                        testflag = True
                    if testflag == True:
                        testcv_s.put(['image', input_img2.copy()])
                        testcv_beat = time.time()
                        testcv_last = time.time()
                    else:
                        testcv_s.put(['PASS', ''])
                        testcv_beat = time.time()

        time.sleep(0.01)



    print('__main__:terminate')

    input_s.put(  [None, None])
    compute_s.put([None, None])
    output_s.put( [None, None])
    speech_s.put( [None, None])
    testcv_s.put( [None, None])

    input_proc.join()
    compute_proc.join()
    output_proc.join()
    speech_proc.join()
    testcv_proc.join()

    print('__main__:Bye!')



