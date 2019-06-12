@ECHO OFF
CALL __setpath.bat

IF NOT EXIST temp         MKDIR temp
IF NOT EXIST temp\log     MKDIR temp\log


ECHO おはようございます。>temp\temp_msg_short.txt
ECHO My password is not your business.>temp\temp_msg_phrase.txt


ECHO マイクロソフト Cognitive Services。>temp\temp_msg_info.txt
ECHO Cognitive Services を利用すれば、>>temp\temp_msg_info.txt
ECHO わずか数行のコードで強力なアルゴリズムを持つ>>temp\temp_msg_info.txt
ECHO インテリジェントなアプリの作成が可能です。>>temp\temp_msg_info.txt

python speech_output_azure.py ja-JP temp/temp_msg_short.txt temp/temp_voice_azure_short.wav
python speech_output_azure.py ja-JP temp/temp_msg_info.txt temp/temp_voice_azure_info.wav
python speech_output_azure.py en-US temp/temp_msg_phrase.txt temp/temp_voice_azure_phrase.wav


ECHO Google Cloud Platform。>temp\temp_msg.txt
ECHO GCP を利用すると、インフラストラクチャの管理やサーバーのプロビジョニング、>>temp\temp_msg.txt
ECHO ネットワークの構成などに起因する負担を軽減することができます。>>temp\temp_msg.txt
ECHO つまり、イノベーターもプログラマーも、自分の本来の仕事に集中できるようになるのです。>>temp\temp_msg.txt

python speech_output_google.py ja temp/temp_msg_short.txt temp/temp_voice.mp3
sox temp/temp_voice.mp3 -r 16000 -b 16 -c 1 temp/temp_voice_google_short.wav
python speech_output_google.py ja temp/temp_msg.txt temp/temp_voice.mp3
sox temp/temp_voice.mp3 -r 16000 -b 16 -c 1 temp/temp_voice_google_info.wav
python speech_output_google.py en temp/temp_msg_phrase.txt temp/temp_voice.mp3
sox temp/temp_voice.mp3 -r 16000 -b 16 -c 1 temp/temp_voice_google_phrase.wav


ECHO Watson とは?。>temp\temp_msg.txt
ECHO IBMは、AIを「Artificial Intelligence（人工知能）」ではなく、>>temp\temp_msg.txt
ECHO 「Augmented Intelligence （拡張知能）」として人間の知識を拡張し増強するものと定義し、>>temp\temp_msg.txt
ECHO ワトソンを中核とするコグニティブ・ソリューションとしてお客様に提供しています。>>temp\temp_msg.txt
ECHO ワトソンは、自然言語処理と機械学習を使用して、>>temp\temp_msg.txt
ECHO 大量の非構造化データから洞察を明らかにするテクノロジー・プラットフォームです。>>temp\temp_msg.txt

python speech_output_watson.py ja temp/temp_msg_short.txt temp/temp_voice.mp3
sox temp/temp_voice.mp3 -r 16000 -b 16 -c 1 temp/temp_voice_watson_short.wav
python speech_output_watson.py ja temp/temp_msg.txt temp/temp_voice.mp3
sox temp/temp_voice.mp3 -r 16000 -b 16 -c 1 temp/temp_voice_watson_info.wav
python speech_output_watson.py en temp/temp_msg_phrase.txt temp/temp_voice.mp3
sox temp/temp_voice.mp3 -r 16000 -b 16 -c 1 temp/temp_voice_watson_phrase.wav


ECHO HOYA Voice Text。>temp\temp_msg.txt
ECHO 誰でも簡単に音声を作成、人の声に限りなく近い圧倒的な肉声感、明瞭感を実現しました。>>temp\temp_msg.txt
ECHO 日本語、英語(アメリカ・イギリス)をはじめ、15言語に対応した多数の話者をラインナップしています。>>temp\temp_msg.txt
ECHO 音声合成は淡々と読むという常識に挑戦、新技術により表現に幅を持たせることが可能になります。>>temp\temp_msg.txt

python speech_output_hoya.py ja temp/temp_msg_short.txt temp/temp_voice_hoya.wav
sox temp/temp_voice_hoya.wav -r 16000 -b 16 -c 1 temp/temp_voice_hoya_short.wav
python speech_output_hoya.py ja temp/temp_msg.txt temp/temp_voice_hoya.wav
sox temp/temp_voice_hoya.wav -r 16000 -b 16 -c 1 temp/temp_voice_hoya_info.wav
python speech_output_hoya.py en temp/temp_msg_phrase.txt temp/temp_voice_hoya.wav
sox temp/temp_voice_hoya.wav -r 16000 -b 16 -c 1 temp/temp_voice_hoya_phrase.wav

PAUSE
