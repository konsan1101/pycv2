@ECHO OFF
CALL __setpath.bat

C:
CD C:\pycv\SpeakerRecognition
IF NOT EXIST usage  MKDIR usage


SET subscription_key=a63270d8e99f426684d3cebed146f52c
rem GOTO SKIP

ECHO;
ECHO;
ECHO ■プロフィール作成■
python Identification\CreateProfile.py           >usage\Identification_CreateProfile.txt
TYPE                                              usage\Identification_CreateProfile.txt
ECHO ↓サンプル
ECHO python Identification\CreateProfile.py       %subscription_key%

ECHO;
ECHO;
ECHO ■プロフィール表示■
python Identification\GetProfile.py              >usage\Identification_GetProfile.txt
TYPE                                              usage\Identification_GetProfile.txt
python Identification\GetProfile.py %subscription_key% 1713992c-7c55-466a-bbc8-051d0557b010

ECHO;
ECHO;
ECHO ■プロフィール一覧■
python Identification\PrintAllProfiles.py      >usage\Identification_PrintAllProfiles.txt
TYPE                                            usage\Identification_PrintAllProfiles.txt
python Identification\PrintAllProfiles.py %subscription_key%

ECHO;
ECHO;
ECHO ■プロフィール削除■
python Identification\DeleteProfile.py           >usage\Identification_DeleteProfile.txt
TYPE                                              usage\Identification_DeleteProfile.txt
ECHO ↓サンプル
ECHO python Identification\DeleteProfile.py       %subscription_key% 00c1db40-dd68-44ac-9b81-cd91a3329cc4

ECHO;
ECHO;
ECHO ■プロフィール音声初期化■
python Identification\ResetEnrollments.py        >usage\Identification_ResetEnrollments.txt
TYPE                                              usage\Identification_ResetEnrollments.txt
python Identification\ResetEnrollments.py %subscription_key% 1713992c-7c55-466a-bbc8-051d0557b010
python Identification\ResetEnrollments.py %subscription_key% 5310cdf7-a74c-4b47-b311-c97176b8502a
python Identification\ResetEnrollments.py %subscription_key% e6cd812d-e903-4856-99c6-f300159ba975
python Identification\ResetEnrollments.py %subscription_key% ad4260cc-9c5b-447e-aaf2-0042c83a15ea
python Identification\ResetEnrollments.py %subscription_key% 43d2d2c9-62b3-44d0-b5d9-db75439aeec7
python Identification\ResetEnrollments.py %subscription_key% 9d90a8d5-89f2-48a7-9219-792d3b2d0be5
python Identification\ResetEnrollments.py %subscription_key% b3a1fb87-0ff4-4550-917d-7e74e83adf00

python Identification\ResetEnrollments.py %subscription_key% e2425804-2425-4a31-a253-c74e27a3fa19
python Identification\ResetEnrollments.py %subscription_key% e2bffa52-e79b-4c18-b5e7-2c2af952a635
python Identification\ResetEnrollments.py %subscription_key% f1ebd2e3-bd04-466d-9af2-f641f1b01bc8

ECHO;
ECHO Waiting...15s
ping localhost -w 1000 -n 15 >>dummy.ping
if exist dummy.ping del dummy.ping

:SKIP

ECHO;
ECHO;
ECHO ■プロフィール音声登録■
python Identification\EnrollProfile.py           >usage\Identification_EnrollProfile.txt
TYPE                                              usage\Identification_EnrollProfile.txt
python Identification\EnrollProfile.py %subscription_key% 1713992c-7c55-466a-bbc8-051d0557b010 ../temp/temp_voice_azure_info.wav True
python Identification\EnrollProfile.py %subscription_key% 5310cdf7-a74c-4b47-b311-c97176b8502a ../temp/temp_voice_google_info.wav True
python Identification\EnrollProfile.py %subscription_key% e6cd812d-e903-4856-99c6-f300159ba975 ../temp/temp_voice_hoya_info.wav True
python Identification\EnrollProfile.py %subscription_key% ad4260cc-9c5b-447e-aaf2-0042c83a15ea ../temp/temp_voice_watson_info.wav True
python Identification\EnrollProfile.py %subscription_key% 43d2d2c9-62b3-44d0-b5d9-db75439aeec7 ../temp/temp_voice_kondou_info.wav True
python Identification\EnrollProfile.py %subscription_key% 43d2d2c9-62b3-44d0-b5d9-db75439aeec7 ../temp/temp_voice_kondou_short.wav True
python Identification\EnrollProfile.py %subscription_key% 9d90a8d5-89f2-48a7-9219-792d3b2d0be5 ../temp/temp_voice_yamanishi_info.wav True
python Identification\EnrollProfile.py %subscription_key% 9d90a8d5-89f2-48a7-9219-792d3b2d0be5 ../temp/temp_voice_yamanishi_short.wav True
python Identification\EnrollProfile.py %subscription_key% b3a1fb87-0ff4-4550-917d-7e74e83adf00 ../temp/temp_voice_minabe_info.wav True
python Identification\EnrollProfile.py %subscription_key% b3a1fb87-0ff4-4550-917d-7e74e83adf00 ../temp/temp_voice_minabe_short.wav True

ECHO;
ECHO Waiting...15s
ping localhost -w 1000 -n 15 >>dummy.ping
if exist dummy.ping del dummy.ping

ECHO;
ECHO;
ECHO ■プロフィール識別■
python Identification\IdentifyFile.py            >usage\Identification_IdentifyFile.txt
TYPE                                              usage\Identification_IdentifyFile.txt
ECHO ↓Azure音声で識別
python Identification\IdentifyFile.py %subscription_key% ../temp/temp_voice_azure_short.wav  True 1713992c-7c55-466a-bbc8-051d0557b010,5310cdf7-a74c-4b47-b311-c97176b8502a,e6cd812d-e903-4856-99c6-f300159ba975,ad4260cc-9c5b-447e-aaf2-0042c83a15ea,43d2d2c9-62b3-44d0-b5d9-db75439aeec7,9d90a8d5-89f2-48a7-9219-792d3b2d0be5,b3a1fb87-0ff4-4550-917d-7e74e83adf00
ECHO ↓Google音声で識別
python Identification\IdentifyFile.py %subscription_key% ../temp/temp_voice_google_short.wav True 1713992c-7c55-466a-bbc8-051d0557b010,5310cdf7-a74c-4b47-b311-c97176b8502a,e6cd812d-e903-4856-99c6-f300159ba975,ad4260cc-9c5b-447e-aaf2-0042c83a15ea,43d2d2c9-62b3-44d0-b5d9-db75439aeec7,9d90a8d5-89f2-48a7-9219-792d3b2d0be5,b3a1fb87-0ff4-4550-917d-7e74e83adf00
ECHO ↓HOYA音声で識別
python Identification\IdentifyFile.py %subscription_key% ../temp/temp_voice_hoya_short.wav True 1713992c-7c55-466a-bbc8-051d0557b010,5310cdf7-a74c-4b47-b311-c97176b8502a,e6cd812d-e903-4856-99c6-f300159ba975,ad4260cc-9c5b-447e-aaf2-0042c83a15ea,43d2d2c9-62b3-44d0-b5d9-db75439aeec7,9d90a8d5-89f2-48a7-9219-792d3b2d0be5,b3a1fb87-0ff4-4550-917d-7e74e83adf00
ECHO ↓Watson音声で識別
python Identification\IdentifyFile.py %subscription_key% ../temp/temp_voice_watson_short.wav True 1713992c-7c55-466a-bbc8-051d0557b010,5310cdf7-a74c-4b47-b311-c97176b8502a,e6cd812d-e903-4856-99c6-f300159ba975,ad4260cc-9c5b-447e-aaf2-0042c83a15ea,43d2d2c9-62b3-44d0-b5d9-db75439aeec7,9d90a8d5-89f2-48a7-9219-792d3b2d0be5,b3a1fb87-0ff4-4550-917d-7e74e83adf00
ECHO ↓近藤音声で識別
python Identification\IdentifyFile.py %subscription_key% ../temp/temp_voice_kondou_short.wav True 1713992c-7c55-466a-bbc8-051d0557b010,5310cdf7-a74c-4b47-b311-c97176b8502a,e6cd812d-e903-4856-99c6-f300159ba975,ad4260cc-9c5b-447e-aaf2-0042c83a15ea,43d2d2c9-62b3-44d0-b5d9-db75439aeec7,9d90a8d5-89f2-48a7-9219-792d3b2d0be5,b3a1fb87-0ff4-4550-917d-7e74e83adf00
ECHO ↓山西音声で識別
python Identification\IdentifyFile.py %subscription_key% ../temp/temp_voice_yamanishi_short.wav True 1713992c-7c55-466a-bbc8-051d0557b010,5310cdf7-a74c-4b47-b311-c97176b8502a,e6cd812d-e903-4856-99c6-f300159ba975,ad4260cc-9c5b-447e-aaf2-0042c83a15ea,43d2d2c9-62b3-44d0-b5d9-db75439aeec7,9d90a8d5-89f2-48a7-9219-792d3b2d0be5,b3a1fb87-0ff4-4550-917d-7e74e83adf00
ECHO ↓三鍋音声で識別
python Identification\IdentifyFile.py %subscription_key% ../temp/temp_voice_minabe_short.wav True 1713992c-7c55-466a-bbc8-051d0557b010,5310cdf7-a74c-4b47-b311-c97176b8502a,e6cd812d-e903-4856-99c6-f300159ba975,ad4260cc-9c5b-447e-aaf2-0042c83a15ea,43d2d2c9-62b3-44d0-b5d9-db75439aeec7,9d90a8d5-89f2-48a7-9219-792d3b2d0be5,b3a1fb87-0ff4-4550-917d-7e74e83adf00

ECHO;
ECHO;
ECHO Enroll最中(IncompleteEnrollment)の場合はエラーになります。
ECHO ENTERで再トライします。
PAUSE;

ECHO;
ECHO;
ECHO ■プロフィール一覧■
python Identification\PrintAllProfiles.py %subscription_key%

GOTO SKIP
