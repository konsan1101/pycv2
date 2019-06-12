@ECHO OFF

CD SpeakerRecognition
python Identification\IdentifyFile_check.py %1%
CD ..
