@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log
IF NOT EXIST temp\images  MKDIR temp\images
IF NOT EXIST temp\voices  MKDIR temp\voices
IF NOT EXIST temp\cache   MKDIR temp\cache
IF NOT EXIST temp\capture MKDIR temp\capture

IF EXIST temp\temp_recSJIS.txt        DEL temp\temp_recSJIS.txt        >temp\dummyV.txt
IF EXIST temp\temp_recTranslator.txt  DEL temp\temp_recTranslator.txt  >temp\dummyV.txt
IF EXIST temp\temp_micON.txt          DEL temp\temp_micON.txt          >temp\dummyV.txt
IF EXIST temp\temp_playSJIS.txt       DEL temp\temp_playSJIS.txt       >temp\dummyV.txt
IF EXIST temp\temp_micWave.wav        DEL temp\temp_micWave.wav        >temp\dummyV.txt


IF EXIST temp\temp_camResult.txt      DEL temp\temp_camResult.txt      >temp\dummyV.txt
ECHO ENTER>temp\temp_camENTER.txt
ECHO CANCEL>temp\temp_camCANCEL.txt

:LOOP

rem python _vision_capture.py 1 360 1920 azure azure   face.xml fullbody.xml azure_capture_face.bat 600

ECHO Google
    python _vision_capture.py 1   0 1280 google google None     None         None                   600

ECHO;
FC temp\temp_camResult.txt temp\temp_camENTER.txt  >temp\dummyV.txt
IF %ERRORLEVEL%@==0@  ECHO ENTER
FC temp\temp_camResult.txt temp\temp_camCANCEL.txt >temp\dummyV.txt
IF %ERRORLEVEL%@==0@  ECHO CANCEL
IF %ERRORLEVEL%@==0@  GOTO FIN

ECHO;
ECHO Waiting...10s
ping localhost -w 1000 -n 10 >temp\dummyV.txt

CLS

ECHO Azure
    python _vision_capture.py 1   0 1280 azure  azure  None     None         None                   600

ECHO;
FC temp\temp_camResult.txt temp\temp_camENTER.txt  >temp\dummyV.txt
IF %ERRORLEVEL%@==0@  ECHO ENTER
FC temp\temp_camResult.txt temp\temp_camCANCEL.txt >temp\dummyV.txt
IF %ERRORLEVEL%@==0@  ECHO CANCEL
IF %ERRORLEVEL%@==0@  GOTO FIN

ECHO;
ECHO Waiting...10s
ping localhost -w 1000 -n 10 >temp\dummyV.txt

CLS
GOTO LOOP

:FIN

ECHO;
ECHO Waiting...20s
ping localhost -w 1000 -n 20 >temp\dummyV.txt

rem PAUSE



