import cv2
from deepface import DeepFace
import mysql.connector
import time
from multiprocessing import Process, Queue
import queue

# Connect to DB
mydb = mysql.connector.connect(
    host="cs1.ucc.ie",
    user="facialrecognition2024",
    password="caipu",
    database="facialrecognition2024"
)

# Function to calculate the % of engagement
def update_engagement(expressions):
    weights = {
        "happy": 1,
        "sad": -2,
        "angry": -2,
        "surprise": 1,
        "fear": -1,
        "neutral": 0
    }
    engagement = sum(weights[expr] * expressions.get(expr, 0) for expr in weights.keys())
    engagement = max(-100, min(100, engagement))
    engagement_percent = round((engagement + 100) / 2 if engagement != 0 else 50, 1)
    return engagement_percent

# Function to regonise the user's face, takes in a queue for real-time insertion and deletion
def facial_recognition(data_queue):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Failed to open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
        # Using the DeepFace algorithm to analyse the face of the user
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        # If face is detected, associate the expression with an emotion in the dictionary, and add the value of it to total_engagement
        if results:
            total_engagement = 0
            for result in results:
                expressions = result['emotion']
                face_engagement = update_engagement(expressions)
                total_engagement += face_engagement
            # Calculate the average engagement
            average_engagement = total_engagement / len(results)
            if average_engagement:
                # Put the figure in the queue
                data_queue.put(average_engagement)

        # Display the frame
        cv2.imshow('Facial Expression Recognition', frame)
        
        # Check for key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        


    cap.release()

# Main function of the program
def main():
    queue = Queue()
    p = Process(target=facial_recognition, args=(queue,))
    p.start()

    total_engagement = 0
    count = 0
    average_engagement_array = []

    while True:
        try:
            # Insert engagement scores into the array
            data = queue.get()
            average_engagement_array.append(data)

            if data == 0.0:
                print("No faces detected!")
            else:
                print("Average Engagement Level:", data)

        except KeyboardInterrupt:
            break

    p.terminate()
    # Calculate the average engagement based on all elements in the session's array
    average = sum(average_engagement_array) / len(average_engagement_array) if average_engagement_array else 0
    print("The average engagement level for this meeting was:", int(average), "%")
    if not average_engagement_array:
        print("No faces detected in the meeting.")
    return average

# Put the average figure into the DB for user feedback
def insert_avg_db(average):
    mycursor = mydb.cursor()
    sql = "INSERT INTO members (percentage) VALUE (%s)"
    val = (int(average),)
    mycursor.execute(sql, val)
    mydb.commit()

if __name__ == "__main__":
    average_engagement = main()
    insert_avg_db(average_engagement)