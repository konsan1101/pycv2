@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log
IF NOT EXIST temp\voices  MKDIR temp\voices
IF NOT EXIST temp\cache   MKDIR temp\cache

IF EXIST temp\temp_recSJIS.txt        DEL temp\temp_recSJIS.txt        >temp\dummyS.txt
IF EXIST temp\temp_recTranslator.txt  DEL temp\temp_recTranslator.txt  >temp\dummyS.txt
IF EXIST temp\temp_micON.txt          DEL temp\temp_micON.txt          >temp\dummyS.txt
IF EXIST temp\temp_playSJIS.txt       DEL temp\temp_playSJIS.txt       >temp\dummyS.txt
IF EXIST temp\temp_micWave.wav        DEL temp\temp_micWave.wav        >temp\dummyS.txt

:LOOP

taskkill /im sox.exe          /f >temp\dummyS.txt
taskkill /im adintool.exe     /f >temp\dummyS.txt
taskkill /im adintool-gui.exe /f >temp\dummyS.txt
taskkill /im julius.exe       /f >temp\dummyS.txt

ECHO ON>temp\temp_micON.txt
    python _speech_allinone.py 0 usb       777 off free   ja en ja translator None Default None
rem python _speech_allinone.py 0 usb       777 off azure  ja en ja translator None Default None
rem python _speech_allinone.py 0 usb       777 off azure  ja en ja speech     None Default None
rem python _speech_allinone.py 0 usb       777 off watson ja en ja translator None Default None

rem python _speech_allinone.py 0 usb       777 on  free   ja en ja translator None Default None
rem python _speech_allinone.py 0 usb       777 on  julius ja en ja translator None Default None
rem python _speech_allinone.py 0 bluetooth 777 off free   ja en ja translator None Default None
rem python _speech_allinone.py 0 bluetooth 777 off free   ja en ja number     None Default None
rem python _speech_allinone.py 0 bluetooth 777 off free   ja en ja speech     None Default None
PAUSE

ECHO;
ECHO Waiting...20s
ping localhost -w 1000 -n 20 >temp\dummyS.txt

CLS
GOTO LOOP



