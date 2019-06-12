#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2
import base64

from requests import Request, Session
#from bs4 import BeautifulSoup
import json



# Google
#GOOGLE_VISION_KEY = 'xx'
GOOGLE_VISION_KEY = 'xx'

def google_vision(image_path):
        global GOOGLE_VISION_KEY

        bin_image = open(image_path, 'rb').read()

        #enc_image = base64.b64encode(bin_image)
        enc_image = base64.b64encode(bin_image).decode("utf-8")

        str_url = "https://vision.googleapis.com/v1/images:annotate?key="

        str_headers = {'Content-Type': 'application/json'}

        str_json_data = {
            'requests': [
                {
                    'image': {
                        'content': enc_image
                    },
                    'features': [
                        {
                            'type': "LABEL_DETECTION",
                            'maxResults': 10
                        },
                        {
                            'type': "TEXT_DETECTION",
                            'maxResults': 10
                        }
                    ]
                }
            ]
        }

        #print("begin request")
        obj_session = Session()
        obj_request = Request("POST",
                              str_url + GOOGLE_VISION_KEY,
                              data=json.dumps(str_json_data),
                              headers=str_headers
                              )
        obj_prepped = obj_session.prepare_request(obj_request)
        obj_response = obj_session.send(obj_prepped,
                                        verify=True,
                                        timeout=60
                                        )
        #print("end request")

        if obj_response.status_code == 200:
            print (obj_response.text)
            #with open('data.json', 'w') as outfile:
            #    json.dump(obj_response.text, outfile)
            return obj_response.text
        else:
            print (obj_response.text)
            return "error"



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

    #if (img=='Test_Image_1.jpg' or img=='CaptureName.jpg') and image_channels == 3:
    #    temp_img = np.zeros((image_height*2,image_width*2,3), np.uint8)
    #    cv2.rectangle(temp_img,(0,0),(image_width*2,image_height*2),(255,255,255),-1)
    #    temp_img[0+image_height/2:image_height/2+image_height, 0+image_width/2:image_width/2+image_width] = image_img.copy()
    #    image_img = cv2.resize(temp_img, (image_width, image_height))

    if image_channels != 1:
        gray_img = cv2.cvtColor(image_img, cv2.COLOR_BGR2GRAY)
    else:
        gray_img = image_img.copy()
    #hist_img = cv2.equalizeHist(gray_img)
    #blur_img = cv2.blur(gray_img, (3,3), 0)
    _, thresh_img = cv2.threshold(gray_img, 140, 255, cv2.THRESH_BINARY)

    temp_img = image_img.copy()
    #temp_img = gray_img.copy()
    #temp_img = thresh_img.copy()
    cv2.imwrite("temp/@" + img, temp_img)

    #cv2.imshow("Base", temp_img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    #jpg_parm = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    #_, img_data = cv2.imencode('.jpg', temp_img, jpg_parm)
    #img_data64 = base64.b64encode(img_data)
    img_data = open("temp/@" + img, 'rb')

    print("main Google AI")
    res = google_vision("temp/@" + img)

    print( "" )
    print( res )
    
    print( "" )
    js = json.loads(res)
    data = js["responses"]
    #print(data)
    #print( json.dumps( data, sort_keys = True, indent = 4) )

    try:
        print( "" )
        s  = "[ LABEL_DETECTION ]"
        f = open(txt, 'w')
        print( s )
        f.writelines( s )

        for t in data:
            for d in t["labelAnnotations"]:

                print(        str(d["description"]) )

                f.writelines( str(d["description"]) )

    except:
        pass
    finally:
        f.close() 

    print( "" )
    print("main Bye!")
    print( "" )



