@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log


python vision_ocr_azure.py vision_ocr__photo.jpg temp/vision_ocr__photo_azure.txt ja
PAUSE

