#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import queue
import threading
import subprocess
import datetime
import time
import codecs

#from selenium import webdriver
import requests as web
import bs4
import urllib.parse

def web_show(search_text):

                            # キーワードを使って検索する
                            list_keywd = [search_text]
                            resp = web.get('https://www.google.co.jp/search?num=10&q=' + '　'.join(list_keywd))
                            resp.raise_for_status()

                            # 取得したHTMLをパースする
                            soup = bs4.BeautifulSoup(resp.text, "html.parser")
                            link_elem01 = soup.select('.r > a')
                            link_elem02 = soup.select('.s > .st')

                            title = link_elem01[0].get_text()
                            title = urllib.parse.unquote(title)

                            print('')
                            print(title)

                            text  = link_elem01[0].get_text()
                            text  = urllib.parse.unquote(text)
                            text  = text.replace('\n', '')

                            print('')
                            print(text)

                            url   = link_elem01[0].get('href')
                            url   = url.replace('/url?q=', '')
                            if url.find('&sa=') >= 0:
                                url = url[:url.find('&sa=')]
                            url   = urllib.parse.unquote(url)
                            url   = urllib.parse.unquote(url)

                            print('')
                            print(url)

                            browser = subprocess.Popen(['_handfree_web_open.bat', url])
                            time.sleep(10)
                            browser.terminate()
                            browser = None

                            browser = subprocess.Popen(['_handfree_web_kill.bat'])
                            time.sleep(2)
                            browser.terminate()
                            browser = None



if __name__ == '__main__':


    web_show(u'姫路城')
    web_show(u'三木市の地図')
    web_show(u'おはようございます')



