import cv2
import numpy as np
import face_recognition
import mss
from mss import mss

# Dictionary to store associations between recognized faces and names
face_names = {}

# Function to recognize faces and associate them with names
def recognize_faces(frame):
    rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB

    # Find all face locations in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    # Find face encodings for each face in the current frame
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    expressions = []

    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        # Compare the current face encoding with known face encodings
        matches = face_recognition.compare_faces(list(face_names.keys()), face_encoding)

        name = "Unknown"
        if True in matches:
            # Find the index of the matched face
            match_index = matches.index(True)
            # Get the name associated with the matched face
            name = list(face_names.values())[match_index]

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Calculate facial expression
        face_landmarks = face_recognition.face_landmarks(rgb_frame, [face_locations[0]])[0]
        mouth = face_landmarks['top_lip'] + face_landmarks['bottom_lip']
        mouth_height = max(mouth, key=lambda point: point[1])[1] - min(mouth, key=lambda point: point[1])[1]

        # Define expression categories based on mouth height
        if mouth_height < 5:
            expression = "Neutral"
        elif mouth_height < 15:
            expression = "Mildly Interested"
        else:
            expression = "Enthusiastic"

        expressions.append(expression)

        # Display the name and expression near the face
        cv2.putText(frame, f"Name: {name}", (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, f"Expression: {expression}", (left, bottom + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame, expressions

# Function to calculate enthusiasm level based on expressions
def calculate_enthusiasm(expressions):
    total_faces = len(expressions)
    enthusiastic_faces = expressions.count("Enthusiastic")
    enthusiasm_percentage = (enthusiastic_faces / total_faces) * 100 if total_faces > 0 else 0
    return enthusiasm_percentage

# Main function to capture screen and perform face recognition
def main():
    with mss() as sct:
        while True:
            # Capture the screen
            monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}  # Adjust resolution as needed
            frame = np.array(sct.grab(monitor))

            # Convert the frame to RGB format
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frame, expressions = recognize_faces(rgb_frame)
            enthusiasm_percentage = calculate_enthusiasm(expressions)

            # Output expressions and enthusiasm percentage
            print("Expressions:", expressions)
            print("Enthusiasm Percentage:", enthusiasm_percentage)

            cv2.imshow('Screen Capture', frame)

            # Check for user input to exit
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
