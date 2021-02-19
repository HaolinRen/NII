
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import cv2
import numpy as np


VIDEO_PATH = 'data/videos/e.webm'

def dist(v0, v1):
    l0 = (v1[0]-v0[0]) * (v1[0]-v0[0])
    l1 = (v1[1]-v0[1]) * (v1[1]-v0[1])
    l2 = (v1[2]-v0[2]) * (v1[2]-v0[2])
    return l0 + l1 + l2

def startVideoRec(videoFilePath, optSize):

    frameArr = []

    video_capture = cv2.VideoCapture(videoFilePath)
    # ret, frame = video_capture.read()
    video_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    videoOutFile = cv2.VideoWriter('output_test.mp4', fourcc, 20.0, (video_width, video_height))

    k = 0

    tempFrame = []

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        
        cv2.imshow('Video', frame)
        
        frameArr.append(frame)

        tempArr = 0
        presentSize = len(frameArr)

        if len(tempFrame) == 0:
            tempFrame = frame
        
        if presentSize > optSize:
            presentSize = optSize
        else:
            continue

        for i in range(video_height):
            for j in range(video_width):
                val0 = frameArr[0][i][j]
                tempFrame[i][j] = (0,0,0)
                k = 0
                for l in range(1, optSize):
                    val1 = frameArr[l][i][j]
                    if dist(val0,val1) < 10:
                        k += 1
                    else:
                        break
                    val0 = val1
                if k == optSize-1:
                    tempFrame[i][j] = val0
                    print('oneframe')

        frameArr = []


        videoOutFile.write(tempFrame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    # videoOutFile.release()
    cv2.destroyAllWindows()



startVideoRec(VIDEO_PATH, 20)

