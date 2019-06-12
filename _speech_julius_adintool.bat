@ECHO OFF

start julius\adintool-gui.exe -in mic -rewind 2000 -headmargin 500 -tailmargin 1000 -lv 1555

      julius\adintool.exe     -in mic -rewind 2000 -headmargin 500 -tailmargin 1000 -lv 1555 -out file -filename temp/voices/julius -startid 1

PAUSE

