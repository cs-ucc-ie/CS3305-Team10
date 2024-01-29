import cv2
from pathlib import Path
from keras.models import load_model
import numpy as np

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

# Load the pre-trained deep learning model for emotion recognition
emotion_model = load_model("path/to/emotion_model.h5")

# Function to recognize facial emotions
def recognize_emotion(face_roi):
    face_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    face_roi = cv2.resize(face_roi, (48, 48))
    face_roi = np.expand_dims(face_roi, axis=0)
    face_roi = face_roi / 255.0  # Normalize
    face_roi = np.reshape(face_roi, (1, 48, 48, 1))

    emotion_prediction = emotion_model.predict(face_roi)
    emotion_label = emotion_labels[np.argmax(emotion_prediction)]
    return emotion_label

# Function to capture and recognize faces in real-time
def capture_and_recognize(model="cnn"):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    cap = cv2.VideoCapture(0)  # Use 0 for the default webcam

    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_roi = frame[y:y + h, x:x + w]
            emotion = recognize_emotion(face_roi)

            # Display emotion on the frame
            cv2.putText(frame, f"Emotion: {emotion}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("Real-time Emotion Recognition", frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_recognize()
