import cv2
from deepface import DeepFace

# Load pre-trained deep learning model for facial expression recognition
model = DeepFace.build_model('Emotion')

def update_engagement(expressions):
    # Define weights for each facial expression
    weights = {
        "happy": 1,
        "sad": -2,
        "angry": -2,
        "surprise": 1,
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

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Detect facial expressions using DeepFace
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        # Initialize empty dictionary to store aggregated expressions
        aggregated_expressions = {}

        # Loop through results for each detected face
        for result in results:
            # Extract expressions and their probabilities
            expressions = result['emotion']

            # Aggregate expressions across all faces
            for expr, prob in expressions.items():
                if expr in aggregated_expressions:
                    aggregated_expressions[expr] += prob
                else:
                    aggregated_expressions[expr] = prob

        # Update user's engagement based on aggregated expressions
        user_engagement = update_engagement(aggregated_expressions)

        # Print engagement level
        print("Engagement Level:", user_engagement)

        # Display the frame
        cv2.imshow('Facial Expression Recognition', frame)

        # Check for key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
