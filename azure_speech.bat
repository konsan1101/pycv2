@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log
IF NOT EXIST temp\images  MKDIR temp\images
IF NOT EXIST temp\voices  MKDIR temp\voices
IF NOT EXIST temp\cache   MKDIR temp\cache
IF NOT EXIST temp\capture MKDIR temp\capture

IF EXIST temp\temp_recSJIS.txt        DEL temp\temp_recSJIS.txt        >temp\dummyAS.txt
IF EXIST temp\temp_recTranslator.txt  DEL temp\temp_recTranslator.txt  >temp\dummyAS.txt
IF EXIST temp\temp_micON.txt          DEL temp\temp_micON.txt          >temp\dummyAS.txt
IF EXIST temp\temp_playSJIS.txt       DEL temp\temp_playSJIS.txt       >temp\dummyAS.txt
IF EXIST temp\temp_micWave.wav        DEL temp\temp_micWave.wav        >temp\dummyAS.txt

ECHO マジックワード
ECHO おはよう、行ってきます、戻りました、お先に

:LOOP

taskkill /im sox.exe          /f >temp\dummyAS.txt
taskkill /im adintool.exe     /f >temp\dummyAS.txt
taskkill /im adintool-gui.exe /f >temp\dummyAS.txt
taskkill /im julius.exe       /f >temp\dummyAS.txt

    ECHO ON>temp\temp_micON.txt
rem python _speech_allinone.py 0 usb 1555 on azure ja ja ja speech None Default azure_speech_id.bat
    python _speech_allinone.py 0 usb 1555 on free  ja ja ja speech None Default azure_speech_id.bat
rem python _handfree_control.py reception None 360 0 usb 1555 on azure

ECHO;
ECHO Waiting...20s
ping localhost -w 1000 -n 20 >temp\dummyAS.txt

CLS
GOTO LOOP



