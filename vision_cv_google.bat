@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log


python vision_cv_google.py vision_cv__photo.jpg temp/vision_cv__photo_google.txt ja
PAUSE

