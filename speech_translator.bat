@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log

ECHO ※mstranslatorは環境により使えない場合があります。
ECHO ※2018/09/27 googletransでエラー発生。
ECHO ※2018/10/12 googletransフォルダのgtoken.pyを入替で対処。
ECHO ※2018/11/30 ggtrans利用に修正。
ECHO ※2018/11/30 ggtrans導入後、googletransお復活したがggtransは言語自動判断付なので以後こちら。

ECHO 自動翻訳エンジンのテストです>temp\temp_recText.txt

ECHO;
python speech_translator_azure.py   ja en temp/temp_recText.txt temp/temp_msga.txt
ECHO;
python speech_translator_google.py  ja en temp/temp_recText.txt temp/temp_msgg1.txt
ECHO;
python speech_translator_goslate.py ja en temp/temp_recText.txt temp/temp_msgg2.txt
ECHO;
python speech_translator_ggtrans.py  ja en temp/temp_recText.txt temp/temp_msgg3.txt
ECHO;
python speech_translator_watson.py  ja en temp/temp_recText.txt temp/temp_msgw.txt
ECHO;
python speech_translator_xazure.py  ja en temp/temp_recText.txt temp/temp_msgax.txt

:LOOP

ECHO;
ECHO;
SET test_rec=
set /P test_rec="自動翻訳したい文字(ja)："
ECHO %test_rec%。>temp\temp_recText.txt
ECHO;
python speech_translator_azure.py   ja en temp/temp_recText.txt temp/temp_msga.txt
ECHO;
python speech_translator_google.py  ja en temp/temp_recText.txt temp/temp_msgg1.txt
ECHO;
python speech_translator_goslate.py ja en temp/temp_recText.txt temp/temp_msgg2.txt
ECHO;
python speech_translator_ggtrans.py  ja en temp/temp_recText.txt temp/temp_msgg3.txt
ECHO;
python speech_translator_watson.py  ja en temp/temp_recText.txt temp/temp_msgw.txt
ECHO;
python speech_translator_xazure.py  ja en temp/temp_recText.txt temp/temp_msgax.txt

GOTO LOOP
