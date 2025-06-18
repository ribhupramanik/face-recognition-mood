import cv2
import sqlite3
from deepface import DeepFace

# Fetch student profile from SQLite database
def get_profile(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.execute("SELECT * FROM STUDENTS WHERE id=?", (id,))
    profile = cursor.fetchone()
    conn.close()
    return profile

def recognize():
    faceDetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(0)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("recognizer/trainingdata.yml")

    CONFIDENCE_THRESHOLD = 60  # Lower = more strict

    print("[INFO] Press 'q' to quit the recognition window.")

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_gray = gray[y:y+h, x:x+w]
            face_gray = cv2.resize(face_gray, (200, 200))
            face_gray = cv2.equalizeHist(face_gray)

            id, conf = recognizer.predict(face_gray)
            roi_color = img[y:y+h, x:x+w]

            # Default emotion
            emotion = "Detecting..."

            try:
                result = DeepFace.analyze(
                    roi_color,
                    actions=['emotion'],
                    enforce_detection=False
                )
                emotion = result[0]['dominant_emotion']
            except Exception as e:
                emotion = "Unknown"

            if conf < CONFIDENCE_THRESHOLD:
                profile = get_profile(id)
                if profile:
                    cv2.putText(img, f"Name: {profile[1]}", (x, y+h+20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 2)
                    cv2.putText(img, f"Age: {profile[2]}", (x, y+h+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 2)
                    cv2.putText(img, f"Mood: {emotion}", (x, y+h+70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,0,255), 2)
                else:
                    cv2.putText(img, "Unknown", (x, y+h+20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
            else:
                cv2.putText(img, "Unknown", (x, y+h+20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)

            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow("Recognizing Faces & Mood", img)
        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
