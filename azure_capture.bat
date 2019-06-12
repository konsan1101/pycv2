@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log
IF NOT EXIST temp\images  MKDIR temp\images
IF NOT EXIST temp\voices  MKDIR temp\voices
IF NOT EXIST temp\cache   MKDIR temp\cache
IF NOT EXIST temp\capture MKDIR temp\capture

IF EXIST temp\temp_recSJIS.txt        DEL temp\temp_recSJIS.txt        >temp\dummyAC.txt
IF EXIST temp\temp_recTranslator.txt  DEL temp\temp_recTranslator.txt  >temp\dummyAC.txt
IF EXIST temp\temp_micON.txt          DEL temp\temp_micON.txt          >temp\dummyAC.txt
IF EXIST temp\temp_playSJIS.txt       DEL temp\temp_playSJIS.txt       >temp\dummyAC.txt
IF EXIST temp\temp_micWave.wav        DEL temp\temp_micWave.wav        >temp\dummyAC.txt

:LOOP

ECHO 受付モードループ
    python _vision_capture.py 1 360 640 azure azure face.xml fullbody.xml azure_capture_face.bat 120
rem python _handfree_control.py reception 0 360 None usb 1555 on azure

ECHO;
ECHO Waiting...20s
ping localhost -w 1000 -n 20 >temp\dummyAC.txt

CLS
GOTO LOOP



