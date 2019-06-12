@ECHO OFF
CALL __setpath.bat

ECHO ※2018/10/12 gTTSでエラー発生。
ECHO ※2018/10/12 gtts_tokenフォルダのgtts_token.pyを入替で対処。
ECHO ※2018/11/30 gTTSでエラー発生。
ECHO ※2018/11/30 gtts_tokenの再インストール(1.1.3)で改善された。

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log


ECHO 音声合成エンジンのテストです。>./temp/temp_msg.txt
ECHO いつもありがとうございます。。>>./temp/temp_msg.txt
python speech_output_azure.py  ja-JP ./temp/temp_msg.txt
python speech_output_google.py ja ./temp/temp_msg.txt
python speech_output_watson.py ja ./temp/temp_msg.txt
python speech_output_hoya.py   ja ./temp/temp_msg.txt
python speech_output_win32.py  ja ./temp/temp_msg.txt

:LOOP

ECHO;
ECHO;
SET test_msg=
set /P test_msg="音声合成したい文字："
ECHO %test_msg%。>./temp/temp_msg.txt
python speech_output_azure.py  ja-JP ./temp/temp_msg.txt
python speech_output_google.py ja ./temp/temp_msg.txt
python speech_output_watson.py ja ./temp/temp_msg.txt
python speech_output_hoya.py   ja ./temp/temp_msg.txt
python speech_output_win32.py  ja ./temp/temp_msg.txt

GOTO LOOP
