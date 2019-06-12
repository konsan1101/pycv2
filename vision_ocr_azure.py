#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2
import base64

import requests
import json



if __name__ == '__main__':
    print("main init")

    img = "CaptureImage.jpg"
    txt = "CaptureText.txt"
    lng = "ja"

    if len(sys.argv)>=2:
        img = sys.argv[1]
    if len(sys.argv)>=3:
        txt = sys.argv[2]
    if len(sys.argv)>=4:
        lng = sys.argv[3]

    print("main image proc")
    image_img = cv2.imread(img, cv2.IMREAD_UNCHANGED)
    if len(image_img.shape) == 3:
        image_height, image_width, image_channels = image_img.shape[:3]
    else:
        image_height, image_width = image_img.shape[:2]
        image_channels = 1

    if (img=='Test_Image_1.jpg' or img=='CaptureName.jpg') and image_channels == 3:
        temp_img = np.zeros((image_height*2,image_width*2,3), np.uint8)
        cv2.rectangle(temp_img,(0,0),(image_width*2,image_height*2),(255,255,255),-1)
        temp_img[0+image_height/2:image_height/2+image_height, 0+image_width/2:image_width/2+image_width] = image_img.copy()
        image_img = cv2.resize(temp_img, (image_width, image_height))

    if image_channels != 1:
        gray_img = cv2.cvtColor(image_img, cv2.COLOR_BGR2GRAY)
    else:
        gray_img = image_img.copy()
    #hist_img = cv2.equalizeHist(gray_img)
    #blur_img = cv2.blur(gray_img, (3,3), 0)
    _, thresh_img = cv2.threshold(gray_img, 140, 255, cv2.THRESH_BINARY)

    #temp_img = thresh_img.copy()
    temp_img = gray_img.copy()
    cv2.imwrite("temp/@" + img, temp_img)

    #cv2.imshow("Base", temp_img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    #jpg_parm = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    #_, img_data = cv2.imencode('.jpg', temp_img, jpg_parm)
    #img_data64 = base64.b64encode(img_data)
    img_data = open("temp/@" + img, 'rb')

    print("main Azure AI")
    res = requests.post(
        'https://eastasia.api.cognitive.microsoft.com/vision/v1.0/ocr',
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': 'xx',
            },
        params = {
            'language': lng,
            'detectOrientation': 'true',
            },
        data = img_data
        )

    print( "" )
    print( res.text )
    
    print( "" )
    js = json.loads(res.text)
    print( json.dumps( js, sort_keys = True, indent = 4) )

    try:
        print( "" )
        s  = "[ OCR ]"
        print( s )
        f = open(txt, 'w')

        for region in js.get('regions'):
            for line in region.get('lines'):
                s = ""
                for word in line.get('words'):
                    s = s + word.get('text')
                print( s )
                f.write( s )

    except:
        pass
    finally:
        f.close() 

    print( "" )
    print("main Bye!")
    print( "" )



