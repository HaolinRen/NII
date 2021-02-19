import face_recognition

from PIL import Image, ImageDraw

fileName = 'data/faces/a staff of JR Tokai bus.jpg'


image = face_recognition.load_image_file(fileName)

sourceImage = Image.open(fileName)

face_landmarks_list = face_recognition.face_landmarks(image)

pil_image = Image.fromarray(image)

d = ImageDraw.Draw(sourceImage)


k = 0
for face_landmarks in face_landmarks_list:
	for i in face_landmarks:
		print(i, len(face_landmarks[i]))
		k += len(face_landmarks[i])
print(k)
    # Print the location of each facial feature in this image
    # for facial_feature in face_landmarks.keys():
    #     print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))

    # # Let's trace out each facial feature in the image with a line!
    # for facial_feature in face_landmarks.keys():
    #     d.line(face_landmarks[facial_feature], width=2)

# sourceImage.show()