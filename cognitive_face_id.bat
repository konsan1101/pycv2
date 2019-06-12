@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log
IF NOT EXIST temp\images  MKDIR temp\images


rem python cognitive_face_id.py
PAUSE

:LOOP

python azure_face_check.py ./temp/kondou/20180131-172828_face.jpg
PAUSE

GOTO LOOP

