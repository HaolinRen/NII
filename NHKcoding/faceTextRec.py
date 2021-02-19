
import face_recognition
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from pytesseract import pytesseract
import cv2
import os
import numpy as np


VIDEO_PATH = 'data/videos/e.webm'

FACE_PATH = 'data/faces/'

LEVEL_INDEX = 0
LEFT_INDEX = 6
TOP_INDEX = 7
WIDTH_INDEX = 8
HEIGHT_INDEX = 9
TEXT_INDEX = 11

known_face_encodings = []
known_face_names = []

def getFaces():
    
    entries = os.listdir(FACE_PATH)
    for oneFace in entries:
        faceName = oneFace.split('.')[0]
        faceImage = face_recognition.load_image_file(FACE_PATH+oneFace)
        faceEncoding = face_recognition.face_encodings(faceImage)
        if len(faceEncoding) > 0:
            known_face_encodings.append(faceEncoding[0])
            known_face_names.append(faceName)
        else:
            print(faceName + ' face can\'t recognise')

def startVideoRec(videoFilePath):
    video_capture = cv2.VideoCapture(videoFilePath)
    ret, frame = video_capture.read()
    video_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    videoOutFile = cv2.VideoWriter('outpute.mp4', fourcc, 20.0, (video_width, video_height))

    face_locations = []
    face_encodings = []
    face_names = []
    textData = ''

    process_this_frame = True

    k = 0

    while True:
        ret, frame = video_capture.read()
        # if process_this_frame:
        #     face_locations = face_recognition.face_locations(frame)
        #     face_encodings = face_recognition.face_encodings(frame, face_locations)
        #     face_names = []
        #     for face_encoding in face_encodings:
        #         # break
        #         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        #         name = "Unknown"
        #         face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        #         best_match_index = np.argmin(face_distances)
        #         if matches[best_match_index]:
        #             name = known_face_names[best_match_index]

        #         face_names.append(name)

        
        #     textData = pytesseract.image_to_data(frame, lang='jpn')
        # process_this_frame = not process_this_frame

        # textBoxes = textData.split('\n')

        # for line in textBoxes:
        #     words = line.split('\t')

        #     if words[0] == '5':
        #         if len(words) > 11:
        #             if words[LEFT_INDEX] != ' ':
        #                 textLeft = int(words[LEFT_INDEX])
        #                 textRight = int(words[WIDTH_INDEX]) + textLeft
        #                 textTop = int(words[TOP_INDEX])
        #                 textBottom = int(words[HEIGHT_INDEX]) + textTop
        #                 cv2.rectangle(frame, (textLeft, textTop), (textRight, textBottom), (0, 255, 0), 2)


        # for top, right, bottom, left in face_locations:
        #     # Draw a box around the face
        #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        #     cv2.rectangle(frame, (left, bottom), (right, bottom), (0, 0, 255), cv2.FILLED)
        #     font = cv2.FONT_HERSHEY_DUPLEX
        #     cv2.putText(frame, name, (left, bottom + 6), font, 0.5, (255, 255, 255), 1)


        # Display the resulting image
        cv2.imshow('Video', frame)
        videoOutFile.write(frame)
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    videoOutFile.release()
    cv2.destroyAllWindows()


# getFaces()


startVideoRec(VIDEO_PATH)

