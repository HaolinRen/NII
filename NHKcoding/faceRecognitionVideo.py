
import face_recognition
import cv2
import numpy as np
import time

video_capture = cv2.VideoCapture('data/videos/d.webm')

tempFrame = []
frameArr = []

video_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))


fourcc = cv2.VideoWriter_fourcc(*'MP4V')
videoOutFile = cv2.VideoWriter('output_test5.mp4', fourcc, 20.0, (video_width, video_height))

start_time = time.time()
frameCount = 0
while video_capture.isOpened():
    ret, frame = video_capture.read()
    if ret != True:
        break
    frameCount += 1
    if len(tempFrame) == 0:
        tempFrame = frame
    face_landmarks_list = face_recognition.face_landmarks(frame)

    # for i in range(video_height):
    #     for j in range(video_width):
    #         tempFrame[i][j] = (255,255,255)

    # # Display the results
    for face_landmarks in face_landmarks_list:
        for landmarks in face_landmarks:
            for point in face_landmarks[landmarks]:
                cv2.circle(frame, point, 2, (0,255,0), -1)
                # frame[point[1]][point[0]] = (0, 255, 0)

    # # cv2.imshow('Video', frameArr)
    # videoOutFile.write(frame)

    # face_locations = face_recognition.face_locations(frame)
    # for top, right, bottom, left in face_locations:
    #     # Draw a box around the face
    #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    #     cv2.rectangle(frame, (left, bottom), (right, bottom), (0, 0, 255), cv2.FILLED)
        
    cv2.imshow('Video', frame)
    # videoOutFile.write(frame)


    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


end_time = time.time()

runningTime = end_time - start_time
print('runningTime ', runningTime)
print('frame sum ', frameCount)
print('fps ', frameCount/runningTime)
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()