@ECHO OFF
C:
CD C:\pycv

rem start julius\julius.exe -input adinnet -C julius/_jconf_20180311gmm.jconf -charconv utf-8 sjis -logfile temp/temp_julius.log -quiet
start julius\julius.exe -input adinnet -C julius/_jconf_20180311gmm.jconf -charconv utf-8 sjis
rem start julius\julius.exe -input adinnet -C julius/_jconf_20180313dnn.jconf -dnnconf julius/julius.dnnconf -charconv utf-8 sjis -logfile temp/temp_julius.log -quiet
rem start julius\julius.exe -input mic     -C julius/_jconf_20180313dnn.jconf -dnnconf julius/julius.dnnconf -charconv utf-8 sjis
ping 1.0.0.0 -w 3000 -n 1 >dummyJ.txt

julius\adintool.exe -in mic -out adinnet -server localhost -rewind 2000 -headmargin 500 -tailmargin 1000 -lv 1555

PAUSE

