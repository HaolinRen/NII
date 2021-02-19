
import face_recognition
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import cv2
import numpy as np


VIDEO_PATH = 'data/videos/v.webm'

def startVideoRec(videoFilePath):
    video_capture = cv2.VideoCapture(videoFilePath)
    process_this_frame = True
    f = 0
    k = 0
    count = 0

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if f > 50:
            face_locations = face_recognition.face_locations(frame)
            if len(face_locations) > 0:
                count += 1
            k += 1
            # face_encodings = face_recognition.face_encodings(frame, face_locations)
            f = 0
        f += 1

        
        process_this_frame = not process_this_frame


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


# getFaces()


startVideoRec(VIDEO_PATH)

print(count/k)
