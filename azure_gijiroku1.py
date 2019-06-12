#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import datetime
import time
import codecs
import glob
import shutil



if __name__ == '__main__':
    print('gijiroku1:init')

    print('')
    print('gijiroku1:start')

    print('')
    print('gijiroku1:check filecount')

    files = {}

    fn = '0n'
    files[fn] = glob.glob('temp/gijiwave_' + fn + '/*')
    fn = '1eq3'
    files[fn] = glob.glob('temp/gijiwave_' + fn + '/*')
    fn = '1eq6'
    files[fn] = glob.glob('temp/gijiwave_' + fn + '/*')
    fn = '1eq9'
    files[fn] = glob.glob('temp/gijiwave_' + fn + '/*')
    fn = '2nv'
    files[fn] = glob.glob('temp/gijiwave_' + fn + '/*')
    fn = '3eq3v'
    files[fn] = glob.glob('temp/gijiwave_' + fn + '/*')
    fn = '3eq6v'
    files[fn] = glob.glob('temp/gijiwave_' + fn + '/*')
    fn = '3eq9v'
    files[fn] = glob.glob('temp/gijiwave_' + fn + '/*')

    maxfn  = ''
    maxlen = 0
    for fn in files:
        if len(files[fn]) != 0:
            print('filecount gijiwave_' + fn, '=', len(files[fn]))
            if maxlen <= len(files[fn]):
                maxfn  = fn
                maxlen = len(files[fn])

    fn = maxfn
    if maxfn != '':
        if maxfn == '0n':
            fn='1eq3'
        if maxfn == '2nv':
            fn='3eq3v'
        print('')
        print('gijiroku1:proc ' + fn + ' (pass = ' + maxfn + ')')
        print('')

    #a=input('pause (press enter) > ')

    if fn != '':

        #XCOPY temp\gijiwave_%fn% temp\gijiwave /Q/R/Y

        print('XCOPY', 'temp/gijiwave_'+fn+'/', 'temp/gijiwave/')
        for f1 in files[fn]:
            f1 = f1.replace('\\', '/')
            f2 = f1
            f2 = f2.replace('/gijiwave_'+fn+'/', '/gijiwave/')
            #print('COPY', f1, f2)
            shutil.copy(f1, f2)

        #COPY temp\temp__gijiroku16_%fn%.wav   temp\temp__gijiroku16.wav

        f1 = 'temp/temp__gijiroku16_' + fn + '.wav'
        f2 = 'temp/temp__gijiroku16.wav'
        print('COPY', f1, f2)
        shutil.copy(f1, f2)

        #sox "temp/temp__gijiroku16.wav"      "temp/temp__gijiroku16.mp3"

        f1 = 'temp/temp__gijiroku16.wav'
        f2 = 'temp/temp__gijiroku16.mp3'
        print('sox', f1, f2)
        sox = subprocess.Popen(['sox', f1, f2, ])
        sox.wait()
        sox.terminate()
        sox = None

        #COPY temp\temp__gijilist16_%fn%.txt   temp\temp__gijilist16.txt

        f1 = 'temp/temp__gijilist16_' + fn + '.txt'
        f2 = 'temp/temp__gijilist16.txt'
        print('COPY', f1, f2)
        shutil.copy(f1, f2)



    print('')
    print('gijiroku1:terminate')

    print('gijiroku1:bye!')



