@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log

python vision_cv_azure.py vision_cv__photo.jpg
pause
