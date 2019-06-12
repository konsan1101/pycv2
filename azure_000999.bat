@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log
IF NOT EXIST temp\voices  MKDIR temp\voices
IF NOT EXIST temp\cache   MKDIR temp\cache
IF NOT EXIST temp\giji    MKDIR temp\giji

IF EXIST temp\temp_recSJIS.txt        DEL temp\temp_recSJIS.txt        >temp\dummyAG.txt
IF EXIST temp\temp_recTranslator.txt  DEL temp\temp_recTranslator.txt  >temp\dummyAG.txt
IF EXIST temp\temp_micON.txt          DEL temp\temp_micON.txt          >temp\dummyAG.txt
IF EXIST temp\temp_playSJIS.txt       DEL temp\temp_playSJIS.txt       >temp\dummyAG.txt
IF EXIST temp\temp_micWave.wav        DEL temp\temp_micWave.wav        >temp\dummyAG.txt


taskkill /im sox.exe          /f >temp\dummyS.txt
taskkill /im adintool.exe     /f >temp\dummyS.txt
taskkill /im adintool-gui.exe /f >temp\dummyS.txt
taskkill /im julius.exe       /f >temp\dummyS.txt

rem python azure_000999.py azure ja
    python azure_000999.py free  ja



PAUSE
