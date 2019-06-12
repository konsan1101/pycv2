#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json

import cognitive_face as CF
import uuid
import glob



if __name__ == '__main__':

    CF.Key.set('xx')
    CF.BaseUrl.set('https://eastasia.api.cognitive.microsoft.com/face/v1.0/')



    print('')
    print('start...')

    #res = CF.person_group.lists()
    #print(res)
    #res = CF.person.lists(group_id)
    #print(res)
    #res = CF.person.delete(group_id, person_id)
    #print(res)
    #res = CF.person_group.delete(group_id)
    #print(res)
    #res = input('>> ')
    #sys.exit()

    #group_id = str(uuid.uuid1())
    #res = CF.person_group.create(group_id)
    #print(res)
    #res = CF.person_group.lists()
    #print(res)
    #res = CF.person.create(group_id, 'test01')
    #print(res)
    #res = CF.person.create(group_id, 'test02')
    #print(res)
    #res = CF.person.create(group_id, 'test03')
    #print(res)
    #res = CF.person.create(group_id, 'test04')
    #print(res)
    #res = CF.person.create(group_id, 'test05')
    #print(res)
    #res = CF.person.lists(group_id)
    #print(res)
    #res = input('>> ')
    #sys.exit()



    print('')
    print('group and person setting...')

    group_id      ='xx'
    group_name    ='test-group'

    person01_id   ='xx'
    person01_name ='kondou'
    person02_id   ='xx'
    person02_name ='yamanishi'
    person03_id   ='xx'
    person03_name ='minabe'
    person04_id   ='xx'
    person04_name ='test04'
    person05_id   ='xx'
    person05_name ='test05'

    res = CF.person_group.update(group_id, group_name)
    res = CF.person.update(group_id, person01_id, person01_name)
    res = CF.person.update(group_id, person02_id, person02_name)
    res = CF.person.update(group_id, person03_id, person03_name)
    res = CF.person.update(group_id, person04_id, person04_name)
    res = CF.person.update(group_id, person05_id, person05_name)



    print('')
    print('new face setting...')

    img_url = 'temp/kondou/20180131-181603_face.jpg'
    res = CF.face.detect(img_url)
    faceId01=res[0]['faceId']
    res = CF.person.add_face(img_url, group_id, person01_id)
    persistedFaceId01=res['persistedFaceId']
    print(person01_name, img_url)

    img_url = 'temp/yamanishi/20180131-173138_face.jpg'
    res = CF.face.detect(img_url)
    faceId02=res[0]['faceId']
    res = CF.person.add_face(img_url, group_id, person02_id)
    persistedFaceId02=res['persistedFaceId']
    print(person02_name, img_url)

    img_url = 'temp/minabe/20180201-183540_face.jpg'
    res = CF.face.detect(img_url)
    faceId03=res[0]['faceId']
    res = CF.person.add_face(img_url, group_id, person03_id)
    persistedFaceId03=res['persistedFaceId']
    print(person03_name, img_url)

    res = CF.person.get(group_id, person01_id)
    persistedFaceIds = res['persistedFaceIds']
    for faceId in persistedFaceIds:
        if faceId != persistedFaceId01:
            res = CF.person.delete_face(group_id, person01_id, faceId)
            #print(res)

    res = CF.person.get(group_id, person02_id)
    persistedFaceIds = res['persistedFaceIds']
    for faceId in persistedFaceIds:
        if faceId != persistedFaceId02:
            res = CF.person.delete_face(group_id, person02_id, faceId)
            #print(res)

    res = CF.person.get(group_id, person03_id)
    persistedFaceIds = res['persistedFaceIds']
    for faceId in persistedFaceIds:
        if faceId != persistedFaceId03:
            res = CF.person.delete_face(group_id, person03_id, faceId)
            #print(res)



    print('')
    print('adding face setting...')

    id  =person01_id
    name=person01_name
    files = glob.glob('temp/' + name + '/*')
    for img_url in files:
        try:
            res = CF.person.add_face(img_url, group_id, id)
            print('OK', img_url)
            #print(res)
        except:
            print('NG', img_url)

    id  =person02_id
    name=person02_name
    files = glob.glob('temp/' + name + '/*')
    for img_url in files:
        try:
            res = CF.person.add_face(img_url, group_id, id)
            print('OK', img_url)
            #print(res)
        except:
            print('NG', img_url)

    id  =person03_id
    name=person03_name
    files = glob.glob('temp/' + name + '/*')
    for img_url in files:
        try:
            res = CF.person.add_face(img_url, group_id, id)
            print('OK', img_url)
            #print(res)
        except:
            print('NG', img_url)




    print('')
    print('group and person list')

    #res = CF.person_group.lists()
    #print(res)
    res = CF.person_group.get(group_id)
    print(res['name'], res['personGroupId'])
    #res = CF.person.lists(group_id)
    #print(res)
    res = CF.person.get(group_id, person01_id)
    print(res['name'], res['personId'])
    res = CF.person.get(group_id, person02_id)
    print(res['name'], res['personId'])
    res = CF.person.get(group_id, person03_id)
    print(res['name'], res['personId'])
    res = CF.person.get(group_id, person04_id)
    print(res['name'], res['personId'])
    res = CF.person.get(group_id, person05_id)
    print(res['name'], res['personId'])

    res = CF.person_group.train(group_id)
    print(res)



    print('')
    print('identify check')

    img_url = 'temp/kondou/20180131-172828_face.jpg'
    print(img_url)
    res = CF.face.detect(img_url)
    faceId=res[0]['faceId']

    #faceIds=[faceId01,faceId02,faceId03]
    #print('')
    #print('face_ids check ' + faceId01,faceId02,faceId03)
    #data = CF.face.find_similars(faceId, face_ids=faceIds, max_candidates_return=5, mode='matchPerson') 
    #print(data)

    print('')
    print('identify...')
    data = CF.face.identify([faceId], person_group_id=group_id, max_candidates_return=5, threshold=0)
    print(data)
    print('')

    persons=data[0]['candidates']
    for person in persons:
        res = CF.person.get(group_id, person['personId'])
        print(res['name'],person['confidence'])

    #res = input('>> ')
    #sys.exit()



