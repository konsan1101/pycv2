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
        'https://eastasia.api.cognitive.microsoft.com/face/v1.0/detect',
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': 'xx',
            },
        params = {
            'returnFaceId': 'false',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender',
            },
        data = open(argv[1], 'rb')
        )

#   print( res.text )
    print( "" )

    j = json.loads(res.text)

    s  = "[ faces ]"
    print( s )
    for face in j:
        s  = ""

        attr = face.get('faceAttributes')
        s += "gender:" + attr.get('gender') + ", age:" + str(attr.get('age'))

        rect = face.get('faceRectangle')
        s += ", top:"    + str(rect.get('top'))   + ", left:" + str(rect.get('left'))
        s += ", width:" + str(rect.get('width')) + ", height:" + str(rect.get('height'))

        print( "  "+ s )

    print( "" )



