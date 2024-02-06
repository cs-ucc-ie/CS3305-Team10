import cv2
import numpy as np
import face_recognition

# Dictionary to store associations between recognized faces and names
face_names = {}

# Function to recognize faces and associate them with names
def recognize_faces(frame):
    rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB

    # Find all face locations in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    # Find face encodings for each face in the current frame
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        # Compare the current face encoding with known face encodings
        matches = face_recognition.compare_faces(list(face_names.keys()), face_encoding)

        name = "Unknown"
        if True in matches:
            # Find the index of the matched face
            match_index = matches.index(True)
            # Get the name associated with the matched face
            name = list(face_names.values())[match_index]

        # Display the name near the face
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    return frame

# Main function to capture screen and perform face recognition
def main():
    screen_capture = cv2.VideoCapture(0)  # Change to the appropriate screen capture device index

    while True:
        ret, frame = screen_capture.read()
        frame = recognize_faces(frame)
        cv2.imshow('Screen Capture', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    screen_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
