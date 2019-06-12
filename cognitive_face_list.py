#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json

import cognitive_face as CF
import uuid



if __name__ == '__main__':

    CF.Key.set('xx')
    CF.BaseUrl.set('https://eastasia.api.cognitive.microsoft.com/face/v1.0/')



    print('')
    print('start...')

    #facelist_id = str(uuid.uuid1())
    #res = CF.face_list.create(facelist_id)
    #print(res)
    #res = CF.face_list.lists()
    #print(res)
    #res = input('>> ')
    #sys.exit()



    print('')
    print('face list setting...')

    facelist_id   ='xx'
    facelist_name ='test-facelist'

    res = CF.face_list.update(facelist_id, facelist_name, '')

    res = CF.face_list.lists()
    for r in res:
        print(r['name'],r['faceListId'])



    print('')
    print('new face setting...')

    img_url = 'temp/kondou/20180131-181603_face.jpg'
    name='kondou'
    res = CF.face.detect(img_url)
    faceId01=res[0]['faceId']
    res = CF.face_list.add_face(img_url, facelist_id, name)
    persistedFaceId01=res['persistedFaceId']
    print(name, img_url)

    res = CF.face_list.get(facelist_id)
    persistedFaces = res['persistedFaces']
    for faces in persistedFaces:
        faceId = faces['persistedFaceId']
        if faceId != persistedFaceId01:
            res = CF.face_list.delete_face(facelist_id, faceId)
            #print(res)

    img_url = 'temp/yamanishi/20180131-173138_face.jpg'
    name='yamanishi'
    res = CF.face.detect(img_url)
    faceId02=res[0]['faceId']
    res = CF.face_list.add_face(img_url, facelist_id, name)
    persistedFaceId02=res['persistedFaceId']
    print(name, img_url)

    img_url = 'temp/minabe/20180201-183540_face.jpg'
    name='minabe'
    res = CF.face.detect(img_url)
    faceId03=res[0]['faceId']
    res = CF.face_list.add_face(img_url, facelist_id, name)
    persistedFaceId03=res['persistedFaceId']
    print(name, img_url)



    print('')
    print('face list')

    res = CF.face_list.get(facelist_id)
    for face in res['persistedFaces']:
        print(face['userData'], face['persistedFaceId'])



    print('')
    print('find_similars')

    img_url = 'temp/kondou/20180131-172828_face.jpg'
    print(img_url)
    res = CF.face.detect(img_url)
    faceId=res[0]['faceId']

    #faceIds=[faceId01,faceId02,faceId03]
    #print('')
    #print('face_ids check ' + faceId01,faceId02,faceId03)
    #data = CF.face.find_similars(faceId, face_ids=faceIds, max_candidates_return=20, mode='matchPerson') 
    #print(data)

    facelistid=facelist_id
    print('')
    print('checking...')
    data = CF.face.find_similars(faceId, face_list_id=facelistid, max_candidates_return=5, mode='matchPerson') 
    print(data)
    print('')

    res = CF.face_list.get(facelist_id)
    for hit in data:
        for face in res['persistedFaces']:
            if str(hit['persistedFaceId'])==str(face['persistedFaceId']):
                print(face['userData'], hit['confidence'])

    res = input('>> ')
    sys.exit()



