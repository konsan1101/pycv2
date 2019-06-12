@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log
IF NOT EXIST temp\voices  MKDIR temp\voices
IF NOT EXIST temp\cache   MKDIR temp\cache

IF EXIST temp\temp_recSJIS.txt        DEL temp\temp_recSJIS.txt        >temp\dummyAP.txt
IF EXIST temp\temp_recTranslator.txt  DEL temp\temp_recTranslator.txt  >temp\dummyAP.txt
IF EXIST temp\temp_micON.txt          DEL temp\temp_micON.txt          >temp\dummyAP.txt
IF EXIST temp\temp_playSJIS.txt       DEL temp\temp_playSJIS.txt       >temp\dummyAP.txt
IF EXIST temp\temp_micWave.wav        DEL temp\temp_micWave.wav        >temp\dummyAP.txt

PAUSE

:LOOP

taskkill /im sox.exe          /f >temp\dummyAP.txt
taskkill /im adintool.exe     /f >temp\dummyAP.txt
taskkill /im adintool-gui.exe /f >temp\dummyAP.txt
taskkill /im julius.exe       /f >temp\dummyAP.txt

    python azure_narration.py azure  ja 1555 azure_narration_sjis.txt
rem python azure_narration.py watson ja 1555 azure_narration_sjis.txt
rem python azure_narration.py google ja 1555 azure_narration_sjis.txt

rem python azure_picking.py azure ja 0
rem python azure_picking.py azure en 0
rem python azure_picking.py azure de 0
rem python azure_picking.py azure fr 0
rem python azure_picking.py azure it 0
rem python azure_picking.py azure zh-CN 0
rem python azure_picking.py free  ko 0
rem python azure_picking.py free  th 0
rem python azure_picking.py free  vi 0

PAUSE

GOTO LOOP
