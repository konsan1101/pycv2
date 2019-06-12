#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import datetime
import time
import codecs
import glob

api      = 'free'
language = 'ja'

def v_speech(recVoice, micctrl):
    #print('v_proc__:init')

    recText = 'temp/temp_recSJIS.txt'
    bakText = 'temp/temp_bakSJIS.txt'
    recTran = 'temp/temp_recTranslator.txt'
    bakTran = 'temp/temp_bakTranslator.txt'
    micWave = 'temp/temp_micWave.wav'

    if os.path.exists(bakTran):
            os.remove(bakTran)
    if os.path.exists(recTran):
            os.remove(recTran)
    if os.path.exists(bakText):
            os.remove(bakText)
    if os.path.exists(recText):
            os.remove(recText)

    if micctrl==False:
        v_micon()

    chktime = time.time()
    while (os.path.exists(micWave)) and (int(time.time() - chktime) < 30):
        time.sleep(0.1)
    if (os.path.exists(micWave)):
        print('v_proc__:Speech No Result! (1)')
        return ''

    #print('v_proc__:start')

    if os.path.exists(recVoice):
        #sox = subprocess.Popen(['sox', recVoice, '-r', '16000', '-b', '16', '-c', '1', micWave, \
        #                        'equalizer', '800', '1.0q', '7', 'tempo', '0.8' ])
        #sox = subprocess.Popen(['sox', recVoice, '-r', '16000', '-b', '16', '-c', '1', micWave,])
        #sox = subprocess.Popen(['sox', '_sound_null.wav', recVoice, '-r', '16000', '-b', '16', '-c', '1', micWave,])
        sox = subprocess.Popen(['sox', recVoice, '-r', '16000', '-b', '16', '-c', '1', micWave,])
        sox.wait()
        sox.terminate()
        sox = None

    if micctrl==True:
        v_micon()
    #time.sleep(2.0)

    #a=input('pause (press enter) > ')

    #print('v_proc__:text wait')

    chktime = time.time()
    while (not os.path.exists(recText)) and (int(time.time() - chktime) < 30):
        time.sleep(0.1)
    if (not os.path.exists(recText)):
        print('v_proc__:Speech Waiting...30s')
    while (not os.path.exists(recText)) and (int(time.time() - chktime) < 60):
        time.sleep(0.1)
    if (not os.path.exists(recText)):
        print('v_proc__:Speech Waiting...60s')
    while (not os.path.exists(recText)) and (int(time.time() - chktime) < 90):
        time.sleep(0.1)
    if (not os.path.exists(recText)):
        print('v_proc__:Speech No Result! (2)')
        if micctrl==True:
            v_micoff()
        return ''

    #print('v_proc__:text hit')
    #print('')

    if micctrl==True:
        v_micoff()

    #if os.path.exists(bakTran):
    #    os.remove(bakTran)
    #if os.path.exists(bakText):
    #    os.remove(bakText)

    chktime = time.time()
    while (os.path.exists(recTran)) and (int(time.time() - chktime) < 5):
        try:
            os.rename(recTran, bakTran)
        except:
            pass
        time.sleep(0.1)
    if (not os.path.exists(bakTran)):
        print('v_proc__:Speech No Result! (3)')
        return ''

    chktime = time.time()
    while (os.path.exists(recText)) and (int(time.time() - chktime) < 5):
        try:
            os.rename(recText, bakText)
        except:
            pass
        time.sleep(0.1)
    if (not os.path.exists(bakText)):
        print('v_proc__:Speech No Result! (4)')
        return ''

    inptxt = ''
    if api != 'azure':
        rt = codecs.open(bakText, 'r', 'shift_jis')
        for t in rt:
            inptxt = (inptxt + ' ' + str(t)).strip()
        rt.close
        rt = None
    else:
        rt = codecs.open(bakTran, 'r', 'utf-8')
        for t in rt:
            inptxt = (inptxt + ' ' + str(t)).strip()
        rt.close
        rt = None

    #print('v_proc__:' + inptxt)

    return inptxt

def v_micon():
    micON   ='temp/temp_micON.txt'
    #print('v_micoff:microphone turn on')
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
    #print('v_micon_:microphone turn off')
    if os.path.exists(micON):
        try:
            os.remove(micON)
        except:
            pass



def proc_file(file, speechText, basebyte, datasize, micctrl):

        file2=file
        file2=file2.replace(u'ゼロ',   '0')
        file2=file2.replace(u'イチ',   '1')
        file2=file2.replace(u'ニイ',   '2')
        file2=file2.replace(u'ニィ',   '2')
        file2=file2.replace(u'ニ',     '2')
        file2=file2.replace(u'サン',   '3')
        file2=file2.replace(u'ヨン',   '4')
        file2=file2.replace(u'ゴオ',   '5')
        file2=file2.replace(u'ゴー',   '5')
        file2=file2.replace(u'ゴ',     '5')
        file2=file2.replace(u'ロク',   '6')
        file2=file2.replace(u'ナナ',   '7')
        file2=file2.replace(u'ハチ',   '8')
        file2=file2.replace(u'キュー', '9')
        file2=file2.replace(u'。',     '' )
        file2=file2.replace('\\',      '/')
        file2=file2.replace('temp/gijiwave/', '')
        file2=file2.replace('_ja_free', '')

        now=datetime.datetime.now()
        stamp=now.strftime('%Y%m%d-%H%M%S')

        if basebyte >=0:
             s=int(basebyte/2/16000)
        else:
             s=int((datasize-44)/2/16000)
        hh=int(s/3600)
        mm=int((s-hh*3600)/60)
        ss=int(s-hh*3600-mm*60)
        tm='{:02}:{:02}:{:02}'.format(hh,mm,ss)

        bakfile=file2[0:len(file2)-4] + '.mp3'

        if datasize<=100:

                    sox = subprocess.Popen(['sox', file, 'gijiroku/9.' + bakfile,])
                    sox.wait()
                    sox.terminate()
                    sox = None

                    print('')
                    print('gijiroku: ' + tm + ', ' + bakfile)

                    try:
                        speechOut  = codecs.open(speechText, 'a', 'shift_jis')
                        speechOut.write(stamp + ', ' + tm + ', ' + bakfile + ', ' + '[!]' + '\r\n')
                        speechOut.close()
                        speechOut = None
                    except:
                        pass

        if datasize>100 and datasize<=1000000:

                    sox = subprocess.Popen(['sox', file, 'gijiroku/9.' + bakfile,])
                    sox.wait()
                    sox.terminate()
                    sox = None

                    print('')
                    print('gijiroku: ' + tm + ', ' + bakfile)

                    try:
                        txt = ''
                        txt = v_speech(file, micctrl)

                        speechOut  = codecs.open(speechText, 'a', 'shift_jis')
                        speechOut.write(stamp + ', ' + tm + ', ' + bakfile + ', ' + '[' + txt + ']' + '\r\n')
                        speechOut.close()
                        speechOut = None
                    except:
                        pass

        if datasize>1000000:
            seq=1
            while seq != 0:

                workf = 'temp/temp__gijiwork' + file[len(file)-4:len(file)]
                sox = subprocess.Popen(['sox', file, workf, 'trim', str((seq-1)*15), '16',])
                sox.wait()
                sox.terminate()
                sox = None

                datasize2=0
                try:
                    rb = open(workf, 'rb')
                    datasize2 = sys.getsizeof(rb.read())
                    rb.close
                    rb = None
                except:
                    pass

                if datasize2>100:

                    now=datetime.datetime.now()
                    stamp=now.strftime('%Y%m%d-%H%M%S')

                    if basebyte >=0:
                        s=int(basebyte/2/16000) + (seq-1)*15
                    else:
                        s=int((datasize2-44)/2/16000)
                    hh=int(s/3600)
                    mm=int((s-hh*3600)/60)
                    ss=int(s-hh*3600-mm*60)
                    tm='{:02}:{:02}:{:02}'.format(hh,mm,ss)

                    bakfile=file2[0:len(file2)-4] + '(' + str(seq) + ').mp3'

                    sox = subprocess.Popen(['sox', workf, 'gijiroku/9.' + bakfile,])
                    sox.wait()
                    sox.terminate()
                    sox = None

                    print('')
                    print('gijiroku: ' + tm + ', ' + bakfile)

                    try:
                        txt = ''
                        txt = v_speech(workf, micctrl)

                        speechOut  = codecs.open(speechText, 'a', 'shift_jis')
                        speechOut.write(stamp + ', ' + tm + ', ' + bakfile + ', ' + '[' + txt + ']' + '\r\n')
                        speechOut.close()
                        speechOut = None
                    except:
                        pass

                    seq += 1

                else:
                    seq = 0



if __name__ == '__main__':
    #global api
    #global language
    #global runmode
    #global micLevel
    print('gijiroku:init')

    api      = 'free'
    language = 'ja'
    outlang  = language
    runmode  = 'speech'
    micLevel = '777'
    if len(sys.argv)>=2:
        api      = sys.argv[1]
    if len(sys.argv)>=3:
        language = sys.argv[2]
        outlang  = language
    if len(sys.argv)>=4:
        runmode  = sys.argv[3]
        if runmode == 'translator':
            outlang  = 'en'
    if len(sys.argv)>=5:
        micLevel = sys.argv[4]

    print('')
    print('gijiroku:api     =' + str(api     ))
    print('gijiroku:language=' + str(language))
    print('gijiroku:runmode =' + str(runmode ))
    print('gijiroku:micLevel=' + str(micLevel))

    speech = None
    #speech=subprocess.Popen(['python', '_speech_allinone.py', 'file', 'usb', '0',      'off', api, language, outlang, 'ja', 'speech', 'temp/temp_micON.txt', 'temp/temp_recSJIS.txt', 'None'])
    #speech=subprocess.Popen(['python', '_speech_allinone.py', 'file', 'usb', '0',      'off', api, language, outlang, 'ja', 'number', 'temp/temp_micON.txt', 'temp/temp_recSJIS.txt', 'None'])
    speech=subprocess.Popen(['python', '_speech_allinone.py', 'file', 'usb', micLevel, 'off', api, language, outlang, 'ja', runmode , 'temp/temp_micON.txt', 'temp/temp_recSJIS.txt', 'None'])

    time.sleep(15)

    print('')
    print('gijiroku:start')

    t=datetime.datetime.now()
    speechText = u'gijiroku/1.認識テキスト_' + t.strftime('%Y%m%d-%H%M%S') + '_' + api + '.txt'
    speechOut  = codecs.open(speechText, 'w', 'shift_jis')
    speechOut.close()
    speechOut = None

    files = glob.glob('temp/gijiwave/*')

    if len(files) > 0:

        basebyte = 0
        for f in files:
            file=f.replace('\\', '/')
            if file[len(file)-4:].lower()=='.wav' or file[len(file)-4:].lower()=='.mp3':

                rb = open(file, 'rb')
                datasize = sys.getsizeof(rb.read())
                rb.close
                rb = None

                proc_file(file, speechText, basebyte, datasize, True)

                basebyte += datasize - 44

    else:
        adintoolsvr = None
        adintoolsvr = subprocess.Popen(['julius/adintool.exe', '-in', 'adinnet', '-out', 'file', '-filename', 'temp/gijiwave/julius', '-startid', '5001',] , \
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        time.sleep(5)

        adintoolexe = None
        adintoolexe = subprocess.Popen(['julius/adintool.exe',     '-in', 'mic', '-rewind', '1111', '-headmargin', '444', '-tailmargin', '666', '-lv', micLevel, '-out', 'adinnet', '-server', 'localhost', '-port', '5530',] , \
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        adintoolgui = None
        adintoolgui = subprocess.Popen(['julius/adintool-gui.exe', '-in', 'mic', '-rewind', '1111', '-headmargin', '444', '-tailmargin', '666', '-lv', micLevel,] , \
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        time.sleep(5)

        basebyte = -1
        while True:
            files = glob.glob('temp/gijiwave/*')

            try:
                for f in files:
                    file=f.replace('\\', '/')
                    if file[len(file)-4:].lower()=='.wav' or file[len(file)-4:].lower()=='.mp3':

                        f1=file
                        f2=file[:len(file)-4] + '.wave'
                        os.rename(f1, f2)
                        os.rename(f2, f1)

                        rb = open(file, 'rb')
                        datasize = sys.getsizeof(rb.read())
                        rb.close
                        rb = None

                        if datasize > 100:
                             proc_file(file, speechText, basebyte, datasize, False)

                        os.remove(file)
            except:
                pass

            time.sleep(0.3)



    print('')
    print('gijiroku:terminate')

    time.sleep(20)
    speech.terminate()

    print('gijiroku:bye!')



