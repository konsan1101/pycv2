@ECHO OFF
C:
CD C:\pycv
IF NOT EXIST temp  MKDIR temp
IF NOT EXIST temp\images  MKDIR temp\images
IF NOT EXIST temp\voices  MKDIR temp\voices
IF NOT EXIST temp\cache   MKDIR temp\cache
IF NOT EXIST temp\capture MKDIR temp\capture

SET PATH=%PATH%;C:\Program Files\sox-14-4-2;
SET PATH=%PATH%;C:\Program Files (x86)\sox-14-4-2;
SET AUDIODRIVER=waveaudio

IF EXIST temp\temp_recSJIS.txt        DEL temp\temp_recSJIS.txt        >temp\dummyHF.txt
IF EXIST temp\temp_recTranslator.txt  DEL temp\temp_recTranslator.txt  >temp\dummyHF.txt
IF EXIST temp\temp_micON.txt          DEL temp\temp_micON.txt          >temp\dummyHF.txt
IF EXIST temp\temp_playSJIS.txt       DEL temp\temp_playSJIS.txt       >temp\dummyHF.txt
IF EXIST temp\temp_micWave.wav        DEL temp\temp_micWave.wav        >temp\dummyHF.txt

:LOOP

taskkill /im sox.exe          /f >temp\dummyHF.txt
taskkill /im adintool.exe     /f >temp\dummyHF.txt
taskkill /im adintool-gui.exe /f >temp\dummyHF.txt
taskkill /im julius.exe       /f >temp\dummyHF.txt
taskkill /im chrome.exe       /f >temp\dummyHF.txt
taskkill /im vlc.exe          /f >temp\dummyHF.txt

 python _handfree_control.py learning None 0   0 bluetooth 1555 off free
rem python _handfree_control.py learning 2 0   0 bluetooth 1555 off free

rem python _handfree_control.py camera     1 0   0 bluetooth 1555 off azure
rem python _handfree_control.py reception  1 360 0 bluetooth 1555 off azure
rem python _handfree_control.py translator 1 0   0 bluetooth 1555 off free
rem python _handfree_control.py learning   1 0   0 bluetooth 1555 off free
rem python _handfree_control.py learning   1 0   0 usb 1555 on free

ECHO Waiting...5s
ping 1.0.0.0 -w 5000 -n 1 >temp\dummyHF.txt
CLS
GOTO LOOP