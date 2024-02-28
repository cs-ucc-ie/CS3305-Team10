import cv2
import numpy as np
from deepface import DeepFace
import pyvirtualcam

# Load pre-trained deep learning model for facial expression recognition
model = DeepFace.build_model('Emotion')

def update_engagement(expressions):
    # Define weights for each facial expression
    weights = {
        "happy": 0.7,
        "sad": -2,
        "angry": -2,
        "surprise": 0.7,
        "fear": -1,
        "neutral": 0
        # Add more expressions and weights as needed
    }

    # Calculate weighted sum of expressions
    engagement = sum(weights[expr] * expressions.get(expr, 0) for expr in weights.keys())

    # Normalize engagement level to the range [-100, 100]
    engagement = max(-100, min(100, engagement))

    # Map engagement level to a percentage between 0 and 100, with neutral set to 50%
    engagement_percent = round((engagement + 100) / 2 if engagement != 0 else 50, 1)

    return engagement_percent

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Failed to open webcam.")
        return

    # Create virtual camera
    try:
        with pyvirtualcam.Camera(width=640, height=480, fps=30) as cam:
            print(f'Using virtual camera: {cam.device}')

            total_engagement = 0
            count = 0

            while True:
                ret, frame = cap.read()

                if not ret:
                    print("Error: Failed to capture frame.")
                    break

                # Detect facial expressions using DeepFace
                results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

                # Check if any face is detected
                if results:
                    # Initialize total engagement for this frame
                    frame_engagement = 0

                    # Loop through results for each detected face
                    for result in results:
                        # Extract expressions and their probabilities
                        expressions = result['emotion']

                        # Calculate engagement for this face
                        face_engagement = update_engagement(expressions)

                        # Accumulate total engagement for this frame
                        frame_engagement += face_engagement

                        # Draw bounding box around the detected face
                        x, y, w, h = result['box']
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    # Calculate average engagement for this frame
                    average_engagement = frame_engagement / len(results)

                    # Print average engagement for this frame
                    print("Average Engagement Level:", average_engagement)

                    # Accumulate total engagement
                    total_engagement += average_engagement
                    count += 1

                else:
                    print("No faces detected!")

                # Resize frame to match virtual camera dimensions
                frame = cv2.resize(frame, (cam.width, cam.height))

                # Send frame to virtual camera
                cam.send(frame[..., ::-1])

                # Check for key press to exit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    except Exception as e:
        print("Error:", e)

    # Release the webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    # Calculate and print the average engagement if faces were detected
    if count > 0:
        average = total_engagement / count
        print("The average engagement level for this meeting was:", int(average), "%")
    else:
        print("No faces detected in the meeting.")


if __name__ == "__main__":
    main()

