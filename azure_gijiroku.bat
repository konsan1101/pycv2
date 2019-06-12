@ECHO OFF
CALL __setpath.bat

IF NOT EXIST gijiroku            MKDIR gijiroku
IF NOT EXIST temp                MKDIR temp
IF NOT EXIST temp\log            MKDIR temp\log
IF NOT EXIST temp\voices         MKDIR temp\voices
IF NOT EXIST temp\cache          MKDIR temp\cache
IF NOT EXIST temp\gijiwave       MKDIR temp\gijiwave
IF NOT EXIST temp\gijiwave_0n    MKDIR temp\gijiwave_0n
IF NOT EXIST temp\gijiwave_1eq3  MKDIR temp\gijiwave_1eq3
IF NOT EXIST temp\gijiwave_1eq6  MKDIR temp\gijiwave_1eq6
IF NOT EXIST temp\gijiwave_1eq9  MKDIR temp\gijiwave_1eq9
IF NOT EXIST temp\gijiwave_2nv   MKDIR temp\gijiwave_2nv
IF NOT EXIST temp\gijiwave_3eq3v MKDIR temp\gijiwave_3eq3v
IF NOT EXIST temp\gijiwave_3eq6v MKDIR temp\gijiwave_3eq6v
IF NOT EXIST temp\gijiwave_3eq9v MKDIR temp\gijiwave_3eq9v

IF EXIST temp\temp_recSJIS.txt        DEL temp\temp_recSJIS.txt        >temp\dummyAG.txt
IF EXIST temp\temp_recTranslator.txt  DEL temp\temp_recTranslator.txt  >temp\dummyAG.txt
IF EXIST temp\temp_micON.txt          DEL temp\temp_micON.txt          >temp\dummyAG.txt
IF EXIST temp\temp_playSJIS.txt       DEL temp\temp_playSJIS.txt       >temp\dummyAG.txt
IF EXIST temp\temp_micWave.wav        DEL temp\temp_micWave.wav        >temp\dummyAG.txt



:RERUN

ECHO;
ECHO 音量音質調整（1=mp3議事録,2=ﾏｲｸ入力議事録,入力無しは再変換）
SET volume=
SET /P volume="入力無しはスキップ："
IF %volume%@==1@  GOTO CPY
IF %volume%@==2@  GOTO REAL
IF %volume%@==@   GOTO SKIP
rem IF %volume%@==@   GOTO SEP
GOTO RERUN

:REAL

ECHO;
ECHO ファイル整理

IF EXIST "gijiroku\*.*"             DEL "gijiroku\*.*"            /Q
IF EXIST "temp\temp__giji*.*"       DEL "temp\temp__giji*.*"      /Q
IF EXIST "temp\gijiwave\*.*"        DEL "temp\gijiwave\*.*"       /Q
IF EXIST "temp\gijiwave_0n\*.*"     DEL "temp\gijiwave_0n\*.*"    /Q
IF EXIST "temp\gijiwave_1eq3\*.*"   DEL "temp\gijiwave_1eq3\*.*"  /Q
IF EXIST "temp\gijiwave_1eq6\*.*"   DEL "temp\gijiwave_1eq6\*.*"  /Q
IF EXIST "temp\gijiwave_1eq9\*.*"   DEL "temp\gijiwave_1eq9\*.*"  /Q
IF EXIST "temp\gijiwave_2nv\*.*"    DEL "temp\gijiwave_2nv\*.*"   /Q
IF EXIST "temp\gijiwave_3eq3v\*.*"  DEL "temp\gijiwave_3eq3v\*.*" /Q
IF EXIST "temp\gijiwave_3eq6v\*.*"  DEL "temp\gijiwave_3eq6v\*.*" /Q
IF EXIST "temp\gijiwave_3eq9v\*.*"  DEL "temp\gijiwave_3eq9v\*.*" /Q
GOTO SKIP

:CPY

ECHO;
ECHO 入力ファイル存在確認
IF NOT EXIST "azure_gijiroku.mp3"  ECHO "Not Found Input File! azure_gijiroku.mp3"
IF NOT EXIST "azure_gijiroku.mp3"  GOTO BYE
ECHO OK

ECHO;
ECHO 音量音質調整（mp3→wav）
IF EXIST "temp\temp__gijiroku*.*" DEL "temp\temp__gijiroku*.*"

ECHO sox "azure_gijiroku.mp3" -r 16000 -b 16 -c 1 "temp/temp__gijiroku16_0n.wav"
     sox "azure_gijiroku.mp3" -r 16000 -b 16 -c 1 "temp/temp__gijiroku16_0n.wav"

ECHO sox "temp/temp__gijiroku16_0n.wav"   "temp/temp__gijiroku16_hilo.wav" highpass 50 lowpass 1200
     sox "temp/temp__gijiroku16_0n.wav"   "temp/temp__gijiroku16_hilo.wav" highpass 50 lowpass 1200

ECHO sox "temp/temp__gijiroku16_hilo.wav" "temp/temp__gijiroku16_2nv.wav" gain -n
     sox "temp/temp__gijiroku16_hilo.wav" "temp/temp__gijiroku16_2nv.wav" gain -n

ECHO sox "temp/temp__gijiroku16_0n.wav"   "temp/temp__gijiroku16_eq3a.wav" equalizer 500 1.0q 3
     sox "temp/temp__gijiroku16_0n.wav"   "temp/temp__gijiroku16_eq3a.wav" equalizer 500 1.0q 3
ECHO sox "temp/temp__gijiroku16_eq3a.wav" "temp/temp__gijiroku16_eq3b.wav" equalizer 400 1.0q 3
     sox "temp/temp__gijiroku16_eq3a.wav" "temp/temp__gijiroku16_eq3b.wav" equalizer 400 1.0q 3
ECHO sox "temp/temp__gijiroku16_eq3b.wav" "temp/temp__gijiroku16_eq3c.wav" equalizer 600 1.0q 3
     sox "temp/temp__gijiroku16_eq3b.wav" "temp/temp__gijiroku16_eq3c.wav" equalizer 600 1.0q 3
ECHO sox "temp/temp__gijiroku16_eq3c.wav" "temp/temp__gijiroku16_1eq3.wav" highpass 50 lowpass 1200
     sox "temp/temp__gijiroku16_eq3c.wav" "temp/temp__gijiroku16_1eq3.wav" highpass 50 lowpass 1200

ECHO sox "temp/temp__gijiroku16_0n.wav"   "temp/temp__gijiroku16_eq6a.wav" equalizer 500 1.0q 6
     sox "temp/temp__gijiroku16_0n.wav"   "temp/temp__gijiroku16_eq6a.wav" equalizer 500 1.0q 6
ECHO sox "temp/temp__gijiroku16_eq6a.wav" "temp/temp__gijiroku16_eq6b.wav" equalizer 400 1.0q 6
     sox "temp/temp__gijiroku16_eq6a.wav" "temp/temp__gijiroku16_eq6b.wav" equalizer 400 1.0q 6
ECHO sox "temp/temp__gijiroku16_eq6b.wav" "temp/temp__gijiroku16_eq6c.wav" equalizer 600 1.0q 6
     sox "temp/temp__gijiroku16_eq6b.wav" "temp/temp__gijiroku16_eq6c.wav" equalizer 600 1.0q 6
ECHO sox "temp/temp__gijiroku16_eq6c.wav" "temp/temp__gijiroku16_1eq6.wav" highpass 50 lowpass 1200
     sox "temp/temp__gijiroku16_eq6c.wav" "temp/temp__gijiroku16_1eq6.wav" highpass 50 lowpass 1200

ECHO sox "temp/temp__gijiroku16_0n.wav"   "temp/temp__gijiroku16_eq9a.wav" equalizer 500 1.0q 9
     sox "temp/temp__gijiroku16_0n.wav"   "temp/temp__gijiroku16_eq9a.wav" equalizer 500 1.0q 9
ECHO sox "temp/temp__gijiroku16_eq9a.wav" "temp/temp__gijiroku16_eq9b.wav" equalizer 400 1.0q 9
     sox "temp/temp__gijiroku16_eq9a.wav" "temp/temp__gijiroku16_eq9b.wav" equalizer 400 1.0q 9
ECHO sox "temp/temp__gijiroku16_eq9b.wav" "temp/temp__gijiroku16_eq9c.wav" equalizer 600 1.0q 9
     sox "temp/temp__gijiroku16_eq9b.wav" "temp/temp__gijiroku16_eq9c.wav" equalizer 600 1.0q 9
ECHO sox "temp/temp__gijiroku16_eq9c.wav" "temp/temp__gijiroku16_1eq9.wav" highpass 50 lowpass 1200
     sox "temp/temp__gijiroku16_eq9c.wav" "temp/temp__gijiroku16_1eq9.wav" highpass 50 lowpass 1200

ECHO sox "temp/temp__gijiroku16_1eq3.wav" "temp/temp__gijiroku16_3eq3v.wav" gain -n
     sox "temp/temp__gijiroku16_1eq3.wav" "temp/temp__gijiroku16_3eq3v.wav" gain -n
ECHO sox "temp/temp__gijiroku16_1eq6.wav" "temp/temp__gijiroku16_3eq6v.wav" gain -n
     sox "temp/temp__gijiroku16_1eq6.wav" "temp/temp__gijiroku16_3eq6v.wav" gain -n
ECHO sox "temp/temp__gijiroku16_1eq9.wav" "temp/temp__gijiroku16_3eq9v.wav" gain -n
     sox "temp/temp__gijiroku16_1eq9.wav" "temp/temp__gijiroku16_3eq9v.wav" gain -n

:SEP

ECHO;
ECHO 最適値自動判断（wav→list）

IF EXIST "gijiroku\*.*"             DEL "gijiroku\*.*"      /Q
IF EXIST "temp\gijiwave\*.*"        DEL "temp\gijiwave\*.*" /Q
IF EXIST "temp\gijiwave_0n\*.*"     DEL "temp\gijiwave_0n\*.*" /Q
IF EXIST "temp\gijiwave_1eq3\*.*"   DEL "temp\gijiwave_1eq3\*.*" /Q
IF EXIST "temp\gijiwave_1eq6\*.*"   DEL "temp\gijiwave_1eq6\*.*" /Q
IF EXIST "temp\gijiwave_1eq9\*.*"   DEL "temp\gijiwave_1eq9\*.*" /Q
IF EXIST "temp\gijiwave_2nv\*.*"    DEL "temp\gijiwave_2nv\*.*" /Q
IF EXIST "temp\gijiwave_3eq3v\*.*"  DEL "temp\gijiwave_3eq3v\*.*" /Q
IF EXIST "temp\gijiwave_3eq6v\*.*"  DEL "temp\gijiwave_3eq6v\*.*" /Q
IF EXIST "temp\gijiwave_3eq9v\*.*"  DEL "temp\gijiwave_3eq9v\*.*" /Q

SET fn=0n
ECHO temp/temp__gijiroku16_%fn%.wav>temp\temp__filelist16.txt
ECHO julius\adintool.exe -in file -filelist temp/temp__filelist16.txt -out file -filename temp/gijiwave_%fn%/julius -startid 1 -rewind 1111 -headmargin 444 -tailmargin 666 -lv 777 -zmean >temp/temp__gijilist16_%fn%.txt
     julius\adintool.exe -in file -filelist temp/temp__filelist16.txt -out file -filename temp/gijiwave_%fn%/julius -startid 1 -rewind 1111 -headmargin 444 -tailmargin 666 -lv 777 -zmean >temp/temp__gijilist16_%fn%.txt

SET fn=1eq3
ECHO temp/temp__gijiroku16_%fn%.wav>temp\temp__filelist16.txt
ECHO julius\adintool.exe -in file -filelist temp/temp__filelist16.txt -out file -filename temp/gijiwave_%fn%/julius -startid 1 -rewind 1111 -headmargin 444 -tailmargin 666 -lv 888 -zmean >temp/temp__gijilist16_%fn%.txt
     julius\adintool.exe -in file -filelist temp/temp__filelist16.txt -out file -filename temp/gijiwave_%fn%/julius -startid 1 -rewind 1111 -headmargin 444 -tailmargin 666 -lv 888 -zmean >temp/temp__gijilist16_%fn%.txt

SET fn=1eq6
ECHO temp/temp__gijiroku16_%fn%.wav>temp\temp__filelist16.txt
ECHO julius\adintool.exe -in file -filelist temp/temp__filelist16.txt -out file -filename temp/gijiwave_%fn%/julius -startid 1 -rewind 1111 -headmargin 444 -tailmargin 666 -lv 999 -zmean >temp/temp__gijilist16_%fn%.txt
     julius\adintool.exe -in file -filelist temp/temp__filelist16.txt -out file -filename temp/gijiwave_%fn%/julius -startid 1 -rewind 1111 -headmargin 444 -tailmargin 666 -lv 999 -zmean >temp/temp__gijilist16_%fn%.txt

SET fn=1eq9
ECHO temp/temp__gijiroku16_%fn%.wav>temp\temp__filelist16.txt
ECHO julius\adintool.exe -in file -filelist temp/temp__filelist16.txt -out file -filename temp/gijiwave_%fn%/julius -startid 1 -rewind 1111 -headmargin 444 -tailmargin 666 -lv 1111 -zmean >temp/temp__gijilist16_%fn%.txt
     julius\adintool.exe -in file -filelist temp/temp__filelist16.txt -out file -filename temp/gijiwave_%fn%/julius -startid 1 -rewind 1111 -headmargin 444 -tailmargin 666 -lv 1111 -zmean >temp/temp__gijilist16_%fn%.txt

SET fn=2nv
ECHO temp/temp__gijiroku16_%fn%.wav>temp\temp__filelist16.txt
ECHO julius\adintool.exe -in file -filelist temp/temp__filelist16.txt -out file -filename temp/gijiwave_%fn%/julius -startid 1 -rewind 1111 -headmargin 444 -tailmargin 666 -lv 1222 -zmean >temp/temp__gijilist16_%fn%.txt
     julius\adintool.exe -in file -filelist temp/temp__filelist16.txt -out file -filename temp/gijiwave_%fn%/julius -startid 1 -rewind 1111 -headmargin 444 -tailmargin 666 -lv 1222 -zmean >temp/temp__gijilist16_%fn%.txt

SET fn=3eq3v
ECHO temp/temp__gijiroku16_%fn%.wav>temp\temp__filelist16.txt
ECHO julius\adintool.exe -in file -filelist temp/temp__filelist16.txt -out file -filename temp/gijiwave_%fn%/julius -startid 1 -rewind 1111 -headmargin 444 -tailmargin 666 -lv 1333 -zmean >temp/temp__gijilist16_%fn%.txt
     julius\adintool.exe -in file -filelist temp/temp__filelist16.txt -out file -filename temp/gijiwave_%fn%/julius -startid 1 -rewind 1111 -headmargin 444 -tailmargin 666 -lv 1333 -zmean >temp/temp__gijilist16_%fn%.txt

SET fn=3eq6v
ECHO temp/temp__gijiroku16_%fn%.wav>temp\temp__filelist16.txt
ECHO julius\adintool.exe -in file -filelist temp/temp__filelist16.txt -out file -filename temp/gijiwave_%fn%/julius -startid 1 -rewind 1111 -headmargin 444 -tailmargin 666 -lv 1444 -zmean >temp/temp__gijilist16_%fn%.txt
     julius\adintool.exe -in file -filelist temp/temp__filelist16.txt -out file -filename temp/gijiwave_%fn%/julius -startid 1 -rewind 1111 -headmargin 444 -tailmargin 666 -lv 1444 -zmean >temp/temp__gijilist16_%fn%.txt

SET fn=3eq9v
ECHO temp/temp__gijiroku16_%fn%.wav>temp\temp__filelist16.txt
ECHO julius\adintool.exe -in file -filelist temp/temp__filelist16.txt -out file -filename temp/gijiwave_%fn%/julius -startid 1 -rewind 1111 -headmargin 444 -tailmargin 666 -lv 1555 -zmean >temp/temp__gijilist16_%fn%.txt
     julius\adintool.exe -in file -filelist temp/temp__filelist16.txt -out file -filename temp/gijiwave_%fn%/julius -startid 1 -rewind 1111 -headmargin 444 -tailmargin 666 -lv 1555 -zmean >temp/temp__gijilist16_%fn%.txt

:SKIP

ECHO;
ECHO 処理データ準備

IF EXIST "gijiroku\*.*"               DEL "gijiroku\*.*"      /Q
IF EXIST "temp\gijiwave\*.*"          DEL "temp\gijiwave\*.*" /Q
IF EXIST "temp\temp__gijiroku16.wav"  DEL "temp\temp__gijiroku16.wav" /Q
IF EXIST "temp\temp__gijiroku16.mp3"  DEL "temp\temp__gijiroku16.mp3" /Q
IF EXIST "temp\temp__gijilist16.txt"  DEL "temp\temp__gijilist16.txt" /Q

rem -------------------------
    python azure_gijiroku1.py
rem -------------------------
rem ECHO Waiting...5s
rem ping localhost -w 1000 -n 5 >>dummy.ping
rem if exist dummy.ping del dummy.ping

rem SET fn=1eq3
rem ECHO XCOPY temp\gijiwave_%fn% temp\gijiwave /Q/R/Y
rem      XCOPY temp\gijiwave_%fn% temp\gijiwave /Q/R/Y
rem ECHO COPY temp\temp__gijiroku16_%fn%.wav   temp\temp__gijiroku16.wav
rem      COPY temp\temp__gijiroku16_%fn%.wav   temp\temp__gijiroku16.wav
rem ECHO sox "temp/temp__gijiroku16.wav"      "temp/temp__gijiroku16.mp3"
rem      sox "temp/temp__gijiroku16.wav"      "temp/temp__gijiroku16.mp3"
rem ECHO COPY temp\temp__gijilist16_%fn%.txt   temp\temp__gijilist16.txt
rem      COPY temp\temp__gijilist16_%fn%.txt   temp\temp__gijilist16.txt

rem IF NOT EXIST "temp\temp__gijiroku16.wav"  ECHO "Internal Error! temp/temp__gijiroku16.wav"
rem IF NOT EXIST "temp\temp__gijiroku16.wav"  GOTO BYE
rem IF NOT EXIST "temp\temp__gijilist16.txt"  ECHO "Internal Error! temp/temp__gijilist16.txt"
rem IF NOT EXIST "temp\temp__gijilist16.txt"  GOTO BYE

IF NOT EXIST "temp\temp__gijiroku16.mp3"  GOTO API

ECHO COPY temp\temp__gijiroku16.mp3 gijiroku\0.入力音声.mp3
     COPY temp\temp__gijiroku16.mp3 gijiroku\0.入力音声.mp3
ECHO COPY temp\temp__gijilist16.txt gijiroku\8.julius変換.txt
     COPY temp\temp__gijilist16.txt gijiroku\8.julius変換.txt

ECHO;
ECHO 処理はクラウドで一気に行います。
ECHO 処理を実行するまえに音量は ☆ 必ず ☆ 確かめてください。（temp/gijiwaveフォルダ）
PAUSE

ECHO;
ECHO 音量は確認しましたね？
ECHO 処理はクラウドで一気に行います。（ファイル数＊０．５円）
PAUSE

:API

ECHO;
ECHO API(julius,azure,free,google,watson)選択（入力無しはfree）
SET api=
SET /P api="julius,azure,free,google,watson："
IF %api%@==@  SET api=free
IF %api%@==julius@  GOTO GO
IF %api%@==azure@   GOTO GO
IF %api%@==free@    GOTO GO
IF %api%@==google@  GOTO GO
IF %api%@==watson@  GOTO GO
GOTO API

:GO
taskkill /im sox.exe          /f >temp\dummyG.txt
taskkill /im adintool.exe     /f >temp\dummyG.txt
taskkill /im adintool-gui.exe /f >temp\dummyG.txt
taskkill /im julius.exe       /f >temp\dummyG.txt

rem python azure_gijiroku2.py %api% ja translator 333
    python azure_gijiroku2.py %api% ja speech 333

ECHO;
ECHO API(julius,azure,free,google,watson)のうち %api% の処理は終了。
PAUSE

GOTO API

:BYE
PAUSE
