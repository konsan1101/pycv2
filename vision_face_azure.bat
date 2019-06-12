@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log


python vision_face_azure.py vision_face__photo.jpg
PAUSE
