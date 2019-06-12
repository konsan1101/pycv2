@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log


ECHO ‚¨‚Í‚æ‚¤‚²‚´‚¢‚Ü‚·B>temp\temp_msg.txt
python speech_output_google.py ja temp/temp_msg.txt temp/temp_voice.mp3
ECHO Good morning,>temp\temp_msg.txt
python speech_output_google.py en temp/temp_msg.txt temp/temp_voice.mp3


:LOOP

ECHO;
ECHO;
SET test_msg=
set /P test_msg="‰¹º‡¬‚µ‚½‚¢•¶ŽšF"
ECHO %test_msg%B>temp\temp_msg.txt

python speech_output_google.py ja temp/temp_msg.txt temp/temp_voice.mp3
sox temp/temp_voice.mp3 -r 16000 -b 16 -c 1 temp/temp_voice.wav
copy temp\temp_voice.wav temp\temp_voice_google_short.wav /Y/V

GOTO LOOP
