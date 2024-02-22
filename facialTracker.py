import numpy as np
import cv2
import dlib
from PIL import ImageGrab
import time
import face_recognition

# Load the pre-trained face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the pre-trained eye cascade classifier
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Load the facial landmark predictor
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def update_engagement(current_engagement, expressions):
    # Define engagement levels for different expressions
    engagement_levels = {
        "neutral": 50,   # Neutral expression indicates moderate engagement
        "smile": 100,    # Smiling indicates high engagement
        "nod": 80,       # Nodding indicates moderate-high engagement
        "frown": 20,     # Frowning indicates low engagement
        "tired": 30      # Tired or expressionless face indicates low engagement
        # Add more expressions and corresponding engagement levels as needed
    }

    # Define time-based factors for decreasing engagement
    time_factors = {
        "bored": -10  # If the user looks bored for too long, decrease engagement
        # Add more time-based factors as needed
    }

    # Calculate weighted average of engagement levels based on observed expressions
    total_weight = 0
    for expression, duration in expressions.items():
        weight = engagement_levels.get(expression, 0) * duration
        current_engagement += weight  # Update current engagement with weighted contribution
        total_weight += duration

    # Apply time-based factors to adjust engagement
    for factor, duration in time_factors.items():
        if factor in expressions:
            current_engagement += duration  # Apply time-based factor to engagement

    if total_weight > 0:
        current_engagement /= total_weight  # Normalize by total duration
    else:
        current_engagement = 50  # Default to 50% if no expressions detected

    # Ensure engagement level stays within range [0, 100]
    current_engagement = max(0, min(100, current_engagement))

    return round(current_engagement)  # Round to the nearest whole number


def print_engagement_update(user_engagement, face_idx):
    print(f"Face {face_idx} - Updated Engagement Percentage: {user_engagement}%")
    return user_engagement

def main():
    user_engagement = {idx: 50 for idx in range(1, 6)}  # Initial engagement level for each face (starts at 50%)
    
    while True:
        # Capture the screen
        frame = np.array(ImageGrab.grab(bbox=(0, 40, 1200, 1200)))
        screen = frame.copy()  # Create a copy for drawing

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Store facial encodings and landmarks for each detected face
        face_encodings = []
        face_landmarks = []

        for idx, (x, y, w, h) in enumerate(faces, start=1):
        # Draw bounding box around the face
            cv2.rectangle(screen, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Extract the region of interest (ROI) for the face
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            # Perform facial landmark detection
            face_image = cv2.cvtColor(roi_color, cv2.COLOR_BGR2RGB)  # Convert to RGB
            face_landmarks = face_recognition.face_landmarks(face_image)

            # Immediate calculation on expressions observed
            expressions_observed = {"neutral": 5, "smile": 3, "nod": 2}
            if idx not in user_engagement:
                user_engagement[idx] = 50  # Initialize engagement for new face
            user_engagement[idx] = update_engagement(user_engagement[idx], expressions_observed)
            print_engagement_update(user_engagement[idx], idx)

        # Display the frame
        cv2.imshow('Face Detection', screen)

        # Check for key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Wait for 2 seconds
        time.sleep(2)

    # Close all OpenCV windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
