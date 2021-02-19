# face verification with the VGGFace2 model
from scipy import misc
from PIL import Image
from numpy import asarray
from numpy import expand_dims

from scipy.spatial.distance import cosine
from mtcnn.mtcnn import MTCNN
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input

import os
import csv

IMAGE_SIZE = 224

FACE_ADDRESS = 'data/faces/'

# extract a single face from a given photograph
def extract_face(filename, required_size=(IMAGE_SIZE, IMAGE_SIZE)):

    # load image from file
    pixels = misc.imread(filename, mode='RGB')
    # create the detector, using default weights
    detector = MTCNN()
    # # detect faces in the image
    results = detector.detect_faces(pixels)
    # # extract the bounding box from the first face

    x1, y1, width, height = results[0]['box']
    # print(x1, y1, width,height)
    x2, y2 = x1 + width, y1 + height
    # # extract the face
    face = pixels[y1:y2, x1:x2]
    # resize pixels to the model size
    image = Image.fromarray(face)

    image = image.resize(required_size) 

    face_array = asarray(image)
    return face_array

MTCNN_DETECTOR = MTCNN()

def getImage(imageName):
    return misc.imread(imageName, mode='RGB')

def getFaces(img):
    return MTCNN_DETECTOR.detect_faces(img)

def getOneFace(img, faceBox):
    x1, y1, width, height = faceBox

    if x1 < 0:
        x1 = 0
    if y1 < 0:
        y1 = 0

    x2, y2 = x1 + width, y1 + height

    face = img[y1:y2, x1:x2]

    image = Image.fromarray(face)

    image = image.resize((IMAGE_SIZE, IMAGE_SIZE)) 

    face_array = asarray(image)

    return face_array

# extract faces and calculate face embeddings for a list of photo files
def get_embeddings(filenames):
    # extract faces

    faces = [extract_face(f) for f in filenames]

    # convert into an array of samples
    samples = asarray(faces, 'float32')

    # prepare the face for the model, e.g. center pixels
    samples = preprocess_input(samples, version=2)
    # create a vggface model
    model = VGGFace(model='resnet50', include_top=False, input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3), pooling='avg')
    # perform prediction
    yhat = model.predict(samples)
    return yhat


MY_MODEL = VGGFace(model='resnet50', include_top=False, input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3), pooling='avg')

def getEmbedding(img, faceBox):
    x1, y1, width, height = faceBox
    if x1 < 0:
        x1 = 0
    if y1 < 0:
        y1 = 0

    x2, y2 = x1 + width, y1 + height

    face = img[y1:y2, x1:x2]

    image = Image.fromarray(face)

    image = image.resize((IMAGE_SIZE, IMAGE_SIZE))

    faces = [asarray(image)]

    samples = asarray(faces, 'float32')

    samples = preprocess_input(samples, version=2)
    yhat = MY_MODEL.predict(samples)

    return yhat[0]

# determine if a candidate face is a match for a known face
def is_match(known_embedding, candidate_embedding, thresh=0.3):
    # calculate distance between embeddings
    score = cosine(known_embedding, candidate_embedding)
    if score <= thresh:
        # print('>face is a Match (%.3f <= %.3f)' % (score, thresh))
        return score
    else:
        return 0


def loadTruthFaces():
    images = os.listdir(FACE_ADDRESS)
    filenames = []
    existEmbedding = {}

    temp = []
    for i in images:
        if i[0] != '.':
            temp.append(i)
            filenames.append(FACE_ADDRESS + i)

    embeddings = get_embeddings(filenames)
    for i in range(len(temp)):
        existEmbedding[temp[i]] = [embeddings[i]]

    return existEmbedding
    # imgSize = len(embeddings)

    # for i in range(imgSize-1):
    #   for j in range(i+1, imgSize):
    #       if i != j:
    #           if is_match(embeddings[i], embeddings[j], 0.3):
    #               print(filenames[i], filenames[j])


def getVideo():
    VIDEO_PATH = '/net/per920a/export/das14a/satoh-lab/haolin/nhk/excerpts'
    PROCESSED_VIDEO_DATA = 'data/videoProcessed.csv'
    VIDEO_NAME_PATH = 'data/printNews.csv'

    videoFileList = {}

    res = []
    isFirstLine = True
    with open(VIDEO_NAME_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if isFirstLine:
                isFirstLine = False
                continue
            videoFileList[row[2]] = 0

    isFirstLine = True

    processedVideoFileList = {}

    # with open(PROCESSED_VIDEO_DATA) as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=';')
    #     for row in csv_reader:
    #         if isFirstLine:
    #             isFirstLine = False
    #             continue
    #         videoName = row[0].split('/')[-1]
    #         processedVideoFileList[videoName] = 0


    videoFiles = os.listdir(VIDEO_PATH)

    for oneVideo in videoFileList:
        if oneVideo not in processedVideoFileList:
            res.append(VIDEO_PATH + '/' + oneVideo)

    print(len(res), 'videos')

    return res


def saveProcessedData(rows):
    fileLines = [['video', 'face_name', 'start_frame', 'end_frame', 'total_frame', 'start_time', 'end_time', 'duration']]
    for a in rows:
        fileLines.append(a)

    with open('data/videoProcessed.csv', mode='w') as saveFile:
        writer = csv.writer(saveFile, delimiter=';', quotechar='"')
        for i in fileLines:
            writer.writerow(i)

def saveData():
    pass


# getVideo()
# loadTruthFaces()


