@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log
IF NOT EXIST temp\images  MKDIR temp\images


python cognitive_face_list.py
PAUSE
