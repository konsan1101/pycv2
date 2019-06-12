#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import queue
import threading
import subprocess
import datetime
import time
import codecs

import requests as web
import bs4
import urllib.parse



def v_output(txt):
    playFile='temp/temp_playSJIS.txt'

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

    #print('v_output__: ' + txt)

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



def sub_extpgm(cn_r,cn_s):
    print('extpgm__:init')

    runmode = cn_r.get()
    camdev  = cn_r.get()
    cn_r.task_done()
    print('extpgm__:runmode=' + str(runmode))
    print('extpgm__:camdev =' + str(camdev ))

    print('extpgm__:start')

    playlist = None
    browser  = None
    while True:
        if cn_r.qsize() > 0:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
            if mode_get is None:
                print('extpgm__:None=break')
                break

            if cn_r.qsize() != 0 or cn_s.qsize() > 2:
                print('speech__: queue overflow warning!',cn_r.qsize(),cn_s.qsize())

            if mode_get != 'RUN':
                cn_s.put(['PASS', ''])
            else:

                if camdev == 'None':
                    recText1='temp/temp_recSJIS.txt'
                    recText2='temp/temp_bakSJIS.txt'
                    recTran1='temp/temp_recTranslator.txt'
                    recTran2='temp/temp_bakTranslator.txt'
                else:
                    recText1='temp/temp_bakSJIS.txt'
                    recText2='temp/temp_oldSJIS.txt'
                    recTran1='temp/temp_bakTranslator.txt'
                    recTran2='temp/temp_oldTranslator.txt'

                if os.path.exists(recText1):
                    if os.path.exists(recText2):
                        try:
                            os.remove(recText2)
                        except:
                            pass
                if os.path.exists(recTran1):
                    if os.path.exists(recTran2):
                        try:
                            os.remove(recTran2)
                        except:
                            pass

                hit_text    = ''
                hit_tran    = ''
                play_cmd    = ''
                browser_cmd = ''

                if os.path.exists(recText1):
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

                    if not os.path.exists(recText2):

                            try:
                                os.rename(recText1, recText2)

                                txt = ''
                                rt = codecs.open(recText2, 'r', 'shift_jis')
                                for t in rt:
                                    txt = (txt + ' ' + str(t)).strip()
                                rt.close
                                rt = None

                                hit_text = txt
                            except:
                                rt = None

                japanese = hit_text.lower()
                english  = hit_tran.lower()
                if english != '':

                    if   english == 'playlist 00' or english == 'playlist 0' \
                      or english == 'bgm' or english == 'garageband':
                        play_cmd =  '_handfree_playlist_00.bat'
                    elif english == 'playlist 01' or english == 'playlist 1' \
                      or english == 'playlist etc' or english == 'playlists etc':
                        play_cmd =  '_handfree_playlist_01.bat'
                    elif english == 'playlist 02' or english == 'playlist 2' \
                      or english == 'babymetal':
                        play_cmd =  '_handfree_playlist_02.bat'
                    elif english == 'playlist 03' or english == 'playlist 3' \
                      or english == 'perfume':
                        play_cmd =  '_handfree_playlist_03.bat'
                    elif english == 'playlist 04' or english == 'playlist 4' \
                      or english == 'kyary pamyu pamyu':
                        play_cmd =  '_handfree_playlist_04.bat'
                    elif english == 'playlist 05' or english == 'playlist 5' \
                      or english == 'one ok rock' or english == 'one ok':
                        play_cmd =  '_handfree_playlist_05.bat'
                    elif english == 'playlist 06' or english == 'playlist 6' \
                      or english == 'end of the world':
                        play_cmd =  '_handfree_playlist_06.bat'
                    elif english == 'end playlist' or english == 'end of bgm' \
                      or english == 'close playlist' or english == 'close bgm':
                        play_cmd =  '_close_'

                    elif english == 'browser':
                        browser_cmd = '_open_'
                    elif english == 'end browser' or english == 'close browser' \
                      or english == 'browser exit':
                        browser_cmd = '_close_'

                    elif english == 'reset':
                        play_cmd    = '_close_'
                        browser_cmd = '_close_'

                if play_cmd == '_close_' or play_cmd != '':
                        playlist = subprocess.Popen(['_handfree_control_kill.bat'])
                        playlist.wait(2000)
                        playlist.terminate()
                        playlist = None
                        time.sleep(1)

                if play_cmd != '':
                    if os.path.exists(play_cmd):
                        playlist = subprocess.Popen([play_cmd])

                if browser_cmd == '_open_':
                    if browser is None:
                        urlx = 'https://www.google.co.jp/'
                        browser = subprocess.Popen(['_handfree_web_open.bat', urlx])

                if browser_cmd == '_close_':
                        browser = subprocess.Popen(['_handfree_web_kill.bat'])
                        browser.wait(2000)
                        browser.terminate()
                        browser = None

                if not browser is None:
                    if browser_cmd == '' and play_cmd == '' and japanese != '':

                        url   = ''
                        title = ''
                        text  = ''

                        if url == '':
                            if english[:9] == 'periscope':
                                url = 'https://www.pscp.tv/'

                        if url == '':
                            try:
                                # キーワードを使って検索する
                                list_keywd = [japanese]
                                resp = web.get('https://www.google.co.jp/search?num=10&q=' + '　'.join(list_keywd))
                                resp.raise_for_status()

                                # 取得したHTMLをパースする
                                soup = bs4.BeautifulSoup(resp.text, "html.parser")
                                link_elem01 = soup.select('.r > a')
                                link_elem02 = soup.select('.s > .st')

                                title = link_elem01[0].get_text()
                                title = urllib.parse.unquote(title)

                                text  = link_elem01[0].get_text()
                                text  = urllib.parse.unquote(text)
                                text  = text.replace('\n', '')

                                url   = link_elem01[0].get('href')
                                url   = url.replace('/url?q=', '')
                                if url.find('&sa=') >= 0:
                                    url = url[:url.find('&sa=')]
                                url   = urllib.parse.unquote(url)
                                url   = urllib.parse.unquote(url)

                                #print(title)
                                #print(text)
                                #print(url)
                            except:
                                pass

                        #browser = subprocess.Popen(['_handfree_web_kill.bat'])
                        #browser.wait(2000)
                        #browser.terminate()
                        #browser = None

                        if url != '':
                            print(url)
                            browser = subprocess.Popen(['_handfree_web_open.bat', url])
                        else:
                            browser = subprocess.Popen(['_handfree_web_open.bat', japanese])

            if not playlist is None:
                try:
                    playlist.wait(0.1)
                    playlist = None
                except:
                    pass

            cn_s.put(['OK', ''])

        if cn_r.qsize() == 0:
            time.sleep(0.03)

    print('extpgm__:terminate')

    playlist = subprocess.Popen(['_handfree_control_kill.bat'])
    playlist.wait(2000)
    if not playlist is None:
        playlist.terminate()
        playlist = None

    browser = subprocess.Popen(['_handfree_web_kill.bat'])
    browser.wait(2000)
    if not browser is None:
        browser.terminate()
        browser = None

    print('extpgm__:end')



def sub_vision(cn_r,cn_s):
    print('vision__:init')

    runmode = cn_r.get()
    camdev  = cn_r.get()
    camrote = cn_r.get()
    cn_r.task_done()
    print('vision__:runmode=' + str(runmode))
    print('vision__:camdev =' + str(camdev ))
    print('vision__:camrote=' + str(camrote))

    print('vision__:start')

    vision = None
    while True:
        if cn_r.qsize() > 0:
            cn_r_get = cn_r.get()
            mode_get = cn_r_get[0]
            data_get = cn_r_get[1]
            cn_r.task_done()
            if mode_get is None:
                print('vision__:None=break')
                break

            if cn_r.qsize() != 0 or cn_s.qsize() > 2:
                print('vision__: queue overflow warning!',cn_r.qsize(),cn_s.qsize())

            if vision is None:
                if camdev != 'None':
                    if runmode == 'translator':
                        vision = subprocess.Popen(['python', '_vision_capture.py', camdev, camrote, \
                                                   '1920', 'cars.xml', 'fullbody.xml', 'None', '3600'])
                    elif runmode == 'learning':
                        vision = subprocess.Popen(['python', '_vision_capture.py', camdev, camrote, \
                                                   '1920', 'cars.xml', 'fullbody.xml', 'None', '3600'])
                    elif runmode == 'reception':
                        vision = subprocess.Popen(['python', '_vision_capture.py', camdev, camrote, \
                                                   '640', 'face.xml', 'fullbody.xml', 'azure_capture_face.bat', '120'])
                    elif runmode == 'camera':
                        vision = subprocess.Popen(['python', '_vision_capture.py', camdev, camrote, \
                                                   '1920', 'None', 'None', 'None', '120'])
                    else:
                        vision = subprocess.Popen(['python', '_vision_capture.py', camdev, camrote, \
                                                   '640', 'None', 'None', 'None', '0'])

            if not vision is None:
                try:
                    vision.wait(0.1)
                    vision = None

                    try:
                        camResult = 'temp/temp_camResult.txt'
                        if os.path.exists(camResult):
                            rt = codecs.open(camResult, 'r', 'utf-8')
                            txt = ''
                            for t in rt:
                                txt = (txt + ' ' + str(t)).strip()
                            rt.close
                            rt = None
                            cn_s.put(['END', ''])
                            break
                    except:
                        pass
                except:
                    pass

            cn_s.put(['OK', ''])

        if cn_r.qsize() == 0:
            time.sleep(0.03)

    print('vision__:terminate')
    if not vision is None:
        vision.terminate()
        vision = None

    print('vision__:end')



def sub_speech(cn_r,cn_s):
    print('speech__:init')

    runmode = cn_r.get()
    micdev  = cn_r.get()
    mictype = cn_r.get()
    miclevel= cn_r.get()
    micguide= cn_r.get()
    api     = cn_r.get()
    cn_r.task_done()
    print('speech__:runmode =' + str(runmode ))
    print('speech__:micdev  =' + str(micdev  ))
    print('speech__:mictype =' + str(mictype ))
    print('speech__:miclevel=' + str(miclevel))
    print('speech__:micguide=' + str(micguide))
    print('speech__:api     =' + str(api     ))

    print('speech__:start')

    speech = None
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

            if speech is None:
                if micdev != 'None':
                    if runmode == 'translator':
                        speech = subprocess.Popen(['python', '_speech_allinone.py', micdev, mictype, miclevel, micguide, \
                                                   api, 'ja', 'en', 'ja', runmode, \
                                                   'temp/temp_micON.txt', 'Default', 'None'])
                    elif runmode == 'learning':
                        speech = subprocess.Popen(['python', '_speech_allinone.py', micdev, mictype, miclevel, micguide, \
                                                   api, 'ja', 'en', 'ja', runmode, \
                                                   'temp/temp_micON.txt', 'Default', 'None'])
                    elif runmode == 'reception':
                        speech = subprocess.Popen(['python', '_speech_allinone.py', micdev, mictype, miclevel, micguide, \
                                                   api, 'ja', 'ja', 'ja', 'speech', \
                                                   'temp/temp_micON.txt', 'Default', 'azure_speech_id.bat'])
                    elif runmode == 'camera':
                        speech = subprocess.Popen(['python', '_speech_allinone.py', micdev, mictype, miclevel, micguide, \
                                                   api, 'ja', 'ja', 'ja', 'speech', \
                                                   'None', 'Default', 'None'])
                    else:
                        speech = subprocess.Popen(['python', '_speech_allinone.py', micdev, mictype, miclevel, micguide, \
                                                   api, 'ja', 'en', 'ja', 'translator', \
                                                   'None', 'Default', 'None'])

            if not speech is None:
                try:
                    speech.wait(0.1)
                    speech = None
                except:
                    pass

            cn_s.put(['OK', ''])

        if cn_r.qsize() == 0:
            time.sleep(0.03)

    print('speech__:terminate')
    if not speech is None:
        speech.terminate()
        speech = None
    print('speech__:end')



if __name__ == '__main__':
    print('handfree:init')
    print('handfree:exsample.py runmode, camdev, camrote, micdev, api,')

    runmode = 'translator'
    camdev  = '0'
    camrote = '0'
    micdev  = '0'
    mictype = 'bluetooth'
    miclevel= '1555'
    micguide= 'on'
    api     = 'free'
    if len(sys.argv)>=2:
        runmode = sys.argv[1]
    if len(sys.argv)>=3:
        camdev  = sys.argv[2]
    if len(sys.argv)>=4:
        camrote = sys.argv[3]
    if len(sys.argv)>=5:
        micdev  = sys.argv[4]
    if len(sys.argv)>=6:
        mictype = sys.argv[5]
    if len(sys.argv)>=7:
        miclevel= sys.argv[6]
    if len(sys.argv)>=8:
        micguide= sys.argv[7]
    if len(sys.argv)>=9:
        api     = sys.argv[8]

    print('')
    print('handfree:runmode =' + str(runmode ))
    print('handfree:camdev  =' + str(camdev  ))
    print('handfree:camrote =' + str(camrote ))
    print('handfree:micdev  =' + str(micdev  ))
    print('handfree:mictype =' + str(mictype ))
    print('handfree:miclevel=' + str(miclevel))
    print('handfree:micguide=' + str(micguide))
    print('handfree:api     =' + str(api     ))

    v_micoff()

    print('')
    print('handfree:start')
    main_start   = time.time()

    vision_s     = queue.Queue()
    vision_r     = queue.Queue()
    vision_proc  = None
    vision_beat  = 0
    vision_skip  = 0
    speech_s     = queue.Queue()
    speech_r     = queue.Queue()
    speech_proc  = None
    speech_beat  = 0
    speech_skip  = 0
    extpgm_s     = queue.Queue()
    extpgm_r     = queue.Queue()
    extpgm_proc  = None
    extpgm_beat  = 0
    extpgm_skip  = 0
    onece = True
    while True:

        # Thread timeout check

        if (vision_r.qsize() == 0) and (vision_beat != 0):
            sec = int(time.time() - vision_beat)
            if sec > 60:
                print('handsfree_:vision_proc 60s')
                #vision_beat = time.time()
                print('handfree:vision_proc break')
                vision_s.put([None, None])
                time.sleep(3.0)
                vision_proc = None
                vision_beat = 0
                vision_skip = 0

        if (speech_r.qsize() == 0) and (speech_beat != 0):
            sec = int(time.time() - speech_beat)
            if sec > 60:
                print('handfree:speech_proc 60s')
                #speech_beat = time.time()
                print('handfree:speech_proc break')
                speech_s.put([None, None])
                time.sleep(3.0)
                speech_proc = None
                speech_beat = 0
                speech_skip = 0

        if (extpgm_r.qsize() == 0) and (extpgm_beat != 0):
            sec = int(time.time() - extpgm_beat)
            if sec > 60:
                print('handfree:extpgm_proc 60s')
                #extpgm_beat = time.time()
                print('handfree:extpgm_proc break')
                extpgm_s.put([None, None])
                time.sleep(3.0)
                extpgm_proc = None
                extpgm_beat = 0
                extpgm_skip = 0

        # Thread start

        if vision_proc is None:
            while vision_s.qsize() > 0:
                dummy = vision_s.get()
            while vision_r.qsize() > 0:
                dummy = vision_r.get()
            vision_proc = threading.Thread(target=sub_vision, args=(vision_s,vision_r,))
            vision_proc.daemon = True
            vision_s.put(runmode)
            vision_s.put(camdev )
            vision_s.put(camrote)
            vision_proc.start()
            time.sleep(5.0)

            vision_s.put(['START', ''])
            vision_beat = time.time()
            vision_skip = 0

        if speech_proc is None:
            while speech_s.qsize() > 0:
                dummy = speech_s.get()
            while speech_r.qsize() > 0:
                dummy = speech_r.get()
            speech_proc = threading.Thread(target=sub_speech, args=(speech_s,speech_r,))
            speech_proc.daemon = True
            speech_s.put(runmode )
            speech_s.put(micdev  )
            speech_s.put(mictype )
            speech_s.put(miclevel)
            speech_s.put(micguide)
            speech_s.put(api     )
            speech_proc.start()
            time.sleep(5.0)

            speech_s.put(['START', ''])
            speech_beat = time.time()
            speech_skip = 0

        if extpgm_proc is None:
            while extpgm_s.qsize() > 0:
                dummy = extpgm_s.get()
            while extpgm_r.qsize() > 0:
                dummy = extpgm_r.get()
            extpgm_proc = threading.Thread(target=sub_extpgm, args=(extpgm_s,extpgm_r,))
            extpgm_proc.daemon = True
            extpgm_s.put(runmode )
            extpgm_s.put(camdev  )
            extpgm_proc.start()
            time.sleep(5.0)

            extpgm_s.put(['START', ''])
            extpgm_beat = time.time()
            extpgm_skip = 0

        # processing

        if vision_r.qsize() > 0:
            vision_get = vision_r.get()
            vision_res = vision_get[0]
            vision_dat = vision_get[1]
            vision_r.task_done()
            if vision_res == 'END':
                break
        if vision_r.qsize() == 0 and vision_s.qsize() == 0:
            vision_skip += 1
        else:
            vision_skip = 0
        if vision_skip > 50:
            vision_s.put(['RUN', ''])
            vision_beat = time.time()
            vision_skip = 0

        if speech_r.qsize() > 0:
            speech_get = speech_r.get()
            speech_res = speech_get[0]
            speech_dat = speech_get[1]
            speech_r.task_done()
            if speech_res == 'END':
                break
        if speech_r.qsize() == 0 and speech_s.qsize() == 0:
            speech_skip += 1
        else:
            speech_skip = 0
        if speech_skip > 50:
            speech_s.put(['RUN', ''])
            speech_beat = time.time()
            speech_skip = 0

        if extpgm_r.qsize() > 0:
            extpgm_get = extpgm_r.get()
            extpgm_res = extpgm_get[0]
            extpgm_dat = extpgm_get[1]
            extpgm_r.task_done()
            if extpgm_res == 'END':
                break
        if extpgm_r.qsize() == 0 and extpgm_s.qsize() == 0:
            extpgm_skip += 1
        else:
            extpgm_skip = 0
        if extpgm_skip > 50:
            extpgm_s.put(['RUN', ''])
            extpgm_beat = time.time()
            extpgm_skip = 0

        if onece == True:
            onece = False
            if micdev != 'None':
                if runmode == 'translator' or runmode == 'learning':
                    #v_output('This is a hands-free control systems,')
                    #v_output('First function is translation of multiple languages,')
                    #if runmode == 'learning':
                    #    v_output('with speech feedback for studying japanese,')
                    #v_output('Second function is select music playlist 0 to 6,')
                    #v_output('Third function is voice control web browser,')
                    v_output('ハンズフリー音声制御システムが開始されました。')
                    v_output('第１機能として、複数言語に対応した音声翻訳ができます。')
                    if runmode == 'learning':
                        v_output('日本語学習できるように音声フィードバックも行います。')
                    v_output('第２機能として、音楽プレイリストのゼロから６を、再生できます。')
                    v_output('第３機能として、ウェブブラウザーを、音声制御できます。')
            time.sleep(3.0)
            v_micon()

        time.sleep(0.01)



    print('')
    print('handfree:terminate')

    vision_s.put([None, None])
    speech_s.put([None, None])
    extpgm_s.put([None, None])

    vision_proc.join()
    speech_proc.join()
    extpgm_proc.join()

    print('')
    print('handfree:bye!')



