# import numpy as np
# from keras.preprocessing import image
# from keras_vggface.vggface import VGGFace
# from keras_vggface import utils


# import cv2

def videoWdithTest():
    videoFile = cv2.VideoCapture('/Users/hren/Workspace/NII/deepLearning/NHKcoding/data/videos/v.webm')
    wd = videoFile.get(3)
    ht = videoFile.get(4)
    print(ht)
    print(wd)

# videoWdithTest()

# tensorflow
 # default : VGG16 , you can use model='resnet50' or 'senet50'

# Change the image path with yours.

# def fileTest():
#     LABELS = np.load('/Users/hren/.keras/models/vggface/rcmalli_vggface_labels_v2.npy')
#     print(LABELS)

# model = VGGFace(model='resnet50', include_top=False)

# img = image.load_img('data/faces/Ichiro OZAWA.jpg', target_size=(224, 224))
# x = image.img_to_array(img)
# x = np.expand_dims(x, axis=0)
# x = utils.preprocess_input(x, version=2) # or version=2

# preds = model.predict(x)
# print(preds)
# print('Predicted:', utils.decode_predictions(preds, top=3))


def run():
    model = VGGFace(model='resnet50')

    images = os.listdir('data/faces')
    res = {}
    for i in images:
        if i[0] != '.':
            res[i] = 'data/faces/' + i
    

    for oneFace in res:
        img = image.load_img(res[oneFace], target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = utils.preprocess_input(x, version=2) # or version=2
        preds = model.predict(x)
        print(oneFace, 'Predicted:', utils.decode_predictions(preds, top=3))



# fileTest()
# run()


print('2014_04_17_21_54.mpg' < '2014_04_22_21_54.mpg')