@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log
IF NOT EXIST temp\voices  MKDIR temp\voices


:LOOP

IF EXIST temp\temp_recText.txt  DEL temp\temp_recText.txt >temp\dummy.txt
python speech_input_watson.py 0 ja temp/temp_recText.txt temp/temp_recWave.wav

IF NOT EXIST temp\temp_recText.txt  GOTO LOOP

SET D=%date:~0,4%%date:~5,2%%date:~8,2%
SET TZ=%time: =0%
SET T=%TZ:~0,2%%TZ:~3,2%%TZ:~6,2%
sox temp/temp_recWave.wav -r 16000 -b 16 -c 1 "temp/voices/%D%-%T%_voice.wav"
COPY temp\temp_recText.txt "temp\voices\%D%-%T%_text.txt" /Y/V >temp\dummy.txt

GOTO LOOP
