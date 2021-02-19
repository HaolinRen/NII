
from verify import *
import time
import cv2
from os import listdir
from os.path import isdir, isfile
import random

TEST_SUM = 2

THREHOLD = 0.28

MIN_FRAME_COUNT = 20

WIDTH_THROLD = 0.1

PRAME_DIST = 10

existIDList = []

idSize = 10

def getRandomID():
    alph = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','f','e','g','h','i','j','k','l', 'm','n','o','p','q','r','s','t','u','v','w','x','y','z']
    lg = len(alph) - 1
    rdName = ''
    for i in range(idSize):
        rdName += alph[random.randint(0, lg)]
    if rdName not in existIDList:
        existIDList.append(rdName)
        return rdName
    else:
        return getRandomID(idSize, existIDList)


def processOneVideo(videoName, truthFaces):

    videoFile = cv2.VideoCapture(videoName)
    frameCount = videoFile.get(cv2.CAP_PROP_FRAME_COUNT)

    frameSum = int(frameCount)

    fps = videoFile.get(cv2.CAP_PROP_FPS)
    duration = int(frameCount/fps)
    k = 1

    lastFaceBox = []
    existFaces = {}
    faceData = []

    faceFrameDict = {}

    lastFrameFaceNum = 0

    lastPercent = 0

    shuffle = 0

    face_counter = 0

    while videoFile.isOpened():
        ret, frame = videoFile.read()
        if ret != True:
            break

        # each 5 frame extract faces from video
        if shuffle < 10:
            shuffle += 1
            continue

        shuffle = 0

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = getFaces(image)

        percent = int(float(k)/frameSum * 100)

        if percent != lastPercent:
            lastPercent = percent
            print(videoName + ' Process ' + str(percent) + '%')

        for oneFace in faces:
            oneFace['isRecognised'] = False
        
        if len(faces) == lastFrameFaceNum:
            followFaces(faces, lastFaceBox)

        faceNameList = processNewFaces(image, faces, existFaces)
        
        for oneName in faceNameList:
            if oneName not in faceFrameDict:
                faceFrameDict[oneName] = []

            faceFrameDict[oneName].append(k)


        lastFaceBox = faces

        lastFrameFaceNum = len(faces)

        k += 10

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        # time.sleep(0.1)


    for oneFace in faceFrameDict:

        faceFrames = faceFrameDict[oneFace]
        lg = len(faceFrames)

        startFrame = 0
        endFrame = 0

        startTime = 0
        endTime = 0
    
        if lg > 1:
            for timeIndex in range(0, lg-1):
                endTimeIndex = timeIndex + 1;
                if startFrame == 0:
                    startFrame = faceFrames[timeIndex]
                if faceFrames[endTimeIndex] - faceFrames[timeIndex] > 60:
                    endFrame = faceFrames[timeIndex]
                    t0 = int(startFrame/k * duration)
                    t1 = int(endFrame/k * duration)
                    faceData.append([videoName, oneFace, startFrame, endFrame, k, t0, t1, t1-t0])
                    startFrame = 0

                if timeIndex == lg-2:
                    if startFrame != 0:
                        endFrame = faceFrames[lg-1]
                        t0 = int(startFrame/k * duration)
                        t1 = int(endFrame/k * duration)
                        faceData.append([videoName, oneFace, startFrame, endFrame, k, t0, t1, t1-t0])

    videoFile.release()
    cv2.destroyAllWindows()

    return faceData

def processVideo(videoName, tfaces):

    videoFile = cv2.VideoCapture(videoName)
    frameCount = videoFile.get(cv2.CAP_PROP_FRAME_COUNT)


    videoWidth = videoFile.get(3)

    frameSum = int(frameCount)

    fps = videoFile.get(cv2.CAP_PROP_FPS)
    duration = int(frameCount/fps)
    k = 1

    lastFaceBox = []
    existFaces = {}
    faceData = []

    faceFrameDict = {}

    lastPercent = 0

    shuffle = 0

    face_counter = 0

    faceEmbdDict = {}

    while videoFile.isOpened():
        ret, frame = videoFile.read()
        if ret != True:
            break

        # each 5 frame extract faces from video
        if shuffle < PRAME_DIST:
            shuffle += 1
            continue

        shuffle = 0
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = getFaces(image)
        percent = int(float(k)/frameSum * 100)
        if percent != lastPercent:
            lastPercent = percent
            print(videoName + ' Process ' + str(percent) + '%')

        for oneFace in faces:
            oneFace['isRecognised'] = False
        
        faces = yhatFaces(faces, videoWidth)
        followFaces(faces, lastFaceBox)

        faceNameList = recogniseFaces(image, faces, existFaces)
        
        for oneName in faceNameList:
            if oneName not in faceFrameDict:
                faceFrameDict[oneName] = []
            faceFrameDict[oneName].append(k)

        lastFaceBox = faces

        k += PRAME_DIST-1

    for oneFace in faceFrameDict:

        faceFrames = faceFrameDict[oneFace]
        lg = len(faceFrames)

        startFrame = 0
        endFrame = 0

        startTime = 0
        endTime = 0
    
        if lg > MIN_FRAME_COUNT:
            faceName = compareTruthFaces(existFaces[oneFace], tfaces)
            if faceName:
                for timeIndex in range(0, lg-1):
                    endTimeIndex = timeIndex + 1;
                    if startFrame == 0:
                        startFrame = faceFrames[timeIndex]
                    if faceFrames[endTimeIndex] - faceFrames[timeIndex] > 60:
                        endFrame = faceFrames[timeIndex]
                        t0 = int(startFrame/k * duration)
                        t1 = int(endFrame/k * duration)
                        faceData.append([videoName, faceName, startFrame, endFrame, k, t0, t1, t1-t0])
                        startFrame = 0

                    if timeIndex == lg-2:
                        if startFrame != 0:
                            endFrame = faceFrames[lg-1]
                            t0 = int(startFrame/k * duration)
                            t1 = int(endFrame/k * duration)
                            faceData.append([videoName, faceName, startFrame, endFrame, k, t0, t1, t1-t0])

    videoFile.release()
    cv2.destroyAllWindows()

    return faceData

def testSimilarity(f0, fDict):
    res = False
    maxVal = 3
    for oneFace in fDict:
        matchVal = is_match(fDict[oneFace], f0, THREHOLD)
        if matchVal > 0:
            if matchVal < maxVal:
                res = oneFace
                maxVal = matchVal
    return res

def compareTruthFaces(unknownFace, tfaces):
    faceRetargetDict = {}
    faceName = testSimilarity(unknownFace, tfaces)
    return faceName

def processNewFaces(img, nfs, exfaces):
    faceNameList = []
    for oneFace in nfs:
        if not oneFace['isRecognised']:
            embedding = getEmbedding(img, oneFace['box'])
            faceName = testSimilarity(embedding, exfaces)

            if faceName:
                if oneFace['rgNum'] >= TEST_SUM:
                    if faceName == oneFace['lastName']:
                        oneFace['isRecognised'] = True
                        oneFace['name'] = faceName
                        faceNameList.append(faceName)
                        exfaces[faceName] = embedding
                    else:
                        oneFace['rgNum'] = 0
                        oneFace['lastName'] = faceName
                else:
                    oneFace['lastName'] = faceName
            else:
                faceName = testSimilarity(embedding, tfaces)

                if faceName:
                    if oneFace['rgNum'] >= TEST_SUM:
                        if faceName == oneFace['lastName']:
                            oneFace['isRecognised'] = True
                            oneFace['name'] = faceName
                            faceNameList.append(faceName)
                            exfaces[faceName] = embedding
                        else:
                            oneFace['rgNum'] = 0
                            oneFace['lastName'] = faceName
                    else:
                        oneFace['lastName'] = faceName
                else:
                    if oneFace['rgNum'] >= TEST_SUM:
                        if oneFace['lastName'] == 'unknown':
                            oneFace['isRecognised'] = True
                            oneFace['name'] = 'unknown'
                    else:
                        oneFace['lastName'] = 'unknown'

            oneFace['rgNum'] += 1
        else:
            if oneFace['name'] != 'unknown':
                faceNameList.append(oneFace['name'])
    return faceNameList

def recogniseFaces(img, nfs, exfaces):
    faceNameList = []
    for oneFace in nfs:
        if not oneFace['isRecognised']:
            embedding = getEmbedding(img, oneFace['box'])
            faceName = testSimilarity(embedding, exfaces)

            if faceName:
                oneFace['isRecognised'] = True
                oneFace['name'] = faceName
            else:
                faceName = getRandomID()
                oneFace['isRecognised'] = True
                oneFace['name'] = faceName

            faceNameList.append(faceName)
            exfaces[faceName] = embedding
        else:
            faceNameList.append(oneFace['name'])
    return faceNameList

def testIsNew(fb0, fb1):
    res = False

    if fb0[0] > fb1[0] + fb1[2] or fb1[0] > fb0[0] + fb0[2]:
        return True
    if fb0[1] > fb1[1] + fb1[3] or fb1[1] > fb0[1] + fb0[3]:
        return True

    return res

def followFaces(faceBox, lfbox):
    for oneFace in faceBox:
        isNewFace = True
        for f2 in lfbox:
            isNewFace = testIsNew(oneFace['box'], f2['box'])
            if not isNewFace:
                if f2['isRecognised']:
                    oneFace['isRecognised'] = True
                    oneFace['name'] = f2['name']
                    break
            
def yhatFaces(faces, videoWidth):
    res = []
    for oneFace in faces:
        wd = oneFace['box'][2]
        if wd / videoWidth > WIDTH_THROLD:
            res.append(oneFace)
    return res


def loadVideo(videoFolderPath, truthFaces, fullData):
    TOP_PATH = '/net/per610a/home/mvp/mvp_db/'
    filepath = TOP_PATH + videoFolderPath
    if isdir(filepath):
        for subFile in listdir(filepath):
            tempFile = filepath + '/' + subFile
            if isdir(tempFile):
                for dataFileList in listdir(tempFile):
                    fullList = tempFile + '/' + dataFileList
                    for dataFile in listdir(fullList):
                        if dataFile < '2014_04_22_21_54.mpg':
                            continue
                        if dataFile[-4:] == '.mpg':
                            fullFilePath = fullList + '/' + dataFile
                            faceData = processOneVideo(fullFilePath)
                            # saveProcessedData(data)

def loadVideoDict(videoFolderPath, truthFaces, fullData):
    TOP_PATH = '/net/per610a/home/mvp/mvp_db/'
    filepath = TOP_PATH + videoFolderPath
    if isdir(filepath):
        for subFile in listdir(filepath):
            tempFile = filepath + '/' + subFile
            if isdir(tempFile):
                for dataFileList in listdir(tempFile):
                    fullList = tempFile + '/' + dataFileList
                    for dataFile in listdir(fullList):
                        if dataFile[-4:] == '.mpg':
                            fullFilePath = fullList + '/' + dataFile
                            faceData = processVideo(fullFilePath, truthFaces)
                            fullData += faceData
                            # saveProcessedData(fullData)

def run():
    videoList = getVideo()
    truthFaces = loadTruthFaces()

    data = []

    k = 1
    for oneVideo in videoList:
        faceData = processOneVideo(oneVideo, truthFaces)
        data += faceData

        saveProcessedData(data)
        print('Processed ' + str(k) + ' videos')
        print('========================================')
        k += 1

def run2():
    newsList = ['hodost-lv']
    data = []
    truthFaces = loadTruthFaces()

    for file in newsList:
        loadVideo(file, truthFaces, data)
        saveProcessedData(data)

def run3():
    newsList = ['news7-lv', 'hodost-lv']
    data = []
    truthFaces = loadTruthFaces()
    for file in newsList:
        loadVideoDict(file, truthFaces, data)

# run()

def test():
    truthFaces = loadTruthFaces()

    faceData = processVideo('/Users/hren/Workspace/NII/deepLearning/NHKcoding/2001_03_16_19_00.mpg', truthFaces)
    saveProcessedData(faceData)

# test()
# run3()

# run2()


