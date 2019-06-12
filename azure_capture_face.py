#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time

import cognitive_face as CF
import numpy as np
import cv2
import datetime



if __name__ == '__main__':
    img_url = 'temp/kondou/20180131-172828_face.jpg'
    if len(sys.argv)>=2:
        img_url = sys.argv[1]

    CF.Key.set('xx')
    CF.BaseUrl.set('https://eastasia.api.cognitive.microsoft.com/face/v1.0/')
    group_id ='xx'



    print(img_url)



    try:
        res = CF.face.detect(img_url)
        faceId=res[0]['faceId']

        print('')
        print('identify...')
        data = CF.face.identify([faceId], person_group_id=group_id, max_candidates_return=5, threshold=0)
        print(data)
        print('')

        first_name      =''
        first_confidence=''
        persons=data[0]['candidates']
        for person in persons:
            res = CF.person.get(group_id, person['personId'])
            print(res['name'],person['confidence'])
            if first_name == '':
                first_name       = res['name']
                first_confidence = person['confidence']

        if first_name != '':
            info_img=cv2.imread(img_url)
            cv2.putText(info_img, first_name           , (20,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255))
            cv2.putText(info_img, str(first_confidence), (20,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
            cv2.namedWindow('Infomation', 1)
            cv2.imshow(     'Infomation', info_img)
            sec=int(datetime.datetime.now().strftime('%S'))
            cv2.moveWindow( 'Infomation', sec*10, 25)

            try:
                if first_confidence > 0.6:
                    fn = os.path.basename(img_url)
                    filename = 'temp/' + first_name + '/hit_' + fn
                    cv2.imwrite(filename,info_img)
            except:
                pass

            cv2.waitKey(10000)

            cv2.destroyWindow('Infomation')

    except:
        pass



