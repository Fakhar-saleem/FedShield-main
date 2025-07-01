import cv2
import face_recognition

def detect_face(text):
    try:
        print("Reading image for comparison")
        img = cv2.imread(f'compare\\{text}\\{text}.jpg')
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_encoding = face_recognition.face_encodings(rgb_img)[0]
        print("Image for comparison read successfully")

        print("Reading received image")
        img2 = cv2.imread(f'received_images\\{text}.jpg')
        rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]
        print("Received image read successfully")

        print("Comparing faces")
        result = face_recognition.compare_faces([img_encoding], img_encoding2)
        print(f"Comparison result: {result[0]}")

        if result[0] == True:
            return 1
        elif result[0] == False:
            return 0
    except Exception as e:
        print(f"Error in detect_face: {e}")
        return 0
