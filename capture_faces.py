# capture_faces.py
import cv2
from database import insert_or_update

def capture_faces(user_id, name, age):
    insert_or_update(user_id, name, age)

    faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    sampleNum = 0

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sampleNum += 1
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))       # Resize to standard size
            face = cv2.equalizeHist(face)             # Improve contrast with histogram equalization
            cv2.imwrite(f'dataset/user.{user_id}.{sampleNum}.jpg', face)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.waitKey(100)
        cv2.imshow("Capturing Face", img)
        cv2.waitKey(1)
        if sampleNum >= 100:
            break

    cam.release()
    cv2.destroyAllWindows()
