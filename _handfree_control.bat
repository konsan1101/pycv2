@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log
IF NOT EXIST temp\images  MKDIR temp\images
IF NOT EXIST temp\voices  MKDIR temp\voices
IF NOT EXIST temp\cache   MKDIR temp\cache
IF NOT EXIST temp\capture MKDIR temp\capture

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
rem taskkill /im vlc.exe          /f >temp\dummyHF.txt

    python _handfree_control.py translator 0 0   1280 0 usb       777 off free
rem python _handfree_control.py translator 0 0   1280 0 usb       777 off azure
rem python _handfree_control.py translator 0 0   1280 0 usb       777 off watson

rem python _handfree_control.py learning   2 0   1280 0 usb       777 on  free

rem python _handfree_control.py camera     1 0   1920 0 bluetooth 777 off azure
rem python _handfree_control.py reception  1 360 1280 0 bluetooth 777 off azure
rem python _handfree_control.py translator 1 0   1280 0 bluetooth 777 off free
rem python _handfree_control.py learning   1 0   1280 0 bluetooth 777 off free
rem python _handfree_control.py learning   1 0   1280 0 usb       777 on  free

ECHO;
ECHO Waiting...5s
ping localhost -w 1000 -n 5 >temp\dummyHF.txt

CLS
GOTO LOOP



