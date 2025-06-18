# train_model.py
import cv2
import numpy as np
import os

def train():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = 'dataset'

    def getImagesWithID(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        IDs = []
        for imagePath in imagePaths:
            gray_img = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
            ID = int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(gray_img)
            IDs.append(ID)
        return faces, IDs

    faces, IDs = getImagesWithID(path)
    recognizer.train(faces, np.array(IDs))
    os.makedirs("recognizer", exist_ok=True)
    recognizer.save('recognizer/trainingdata.yml')
