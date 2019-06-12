#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import json



if __name__ == '__main__':
    argv = sys.argv
    if len(argv) == 1:
        print('Usage: # python %s [filename]' % argv[0])
        quit()

    res = requests.post(
        'https://eastasia.api.cognitive.microsoft.com/vision/v1.0/analyze',
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': 'xx',
            },
        params = {
            'visualFeatures': 'Categories,Description',
            'language': 'ja',
            },
        data = open(argv[1], 'rb')
        )

#   print(res.text)
    print( "" )

    js = json.loads(res.text)

    s  = "[ categories ]"
    print( s )
    s  = ""
    for names in js.get('categories'):
        s  += str(names.get('name')).replace('_',' ') + " , "
    print( "  " + s )
    print( "" )

    s  = "[ captions ]"
    print( s )
    for texts in js.get('description').get('captions'):
        s  = str(texts.get('text'))
        print( "  " + s )
    print( "" )

    s  = "[ description ]"
    print( s )
    s  = ""
    j  = ""
    for tag in js.get('description').get('tags'):
        s  += str(tag) + " , "
    print( "  " + s )
    print( "" )



