import tkinter as tk
import mysql.connector

def add_name():
    name = entry.get()
    if name:
        label.config(text=f"Hello, {name}!")
        
        # Save the name to the MySQL database
        save_to_database(name)
        
        root.after(2000, root.destroy)  # Close the window after 2000 milliseconds (2 seconds)

def save_to_database(name):
    try:
        # Database connector
        mydb = mysql.connector.connect(
            host="cs1.ucc.ie",
            user="facialrecognition2024",
            password="caipu",
            database="facialrecognition2024"
            )
        
        mycursor = mydb.cursor()
        
        # Execute an SQL query to insert the name into the 'names' table
        query = "INSERT INTO costumers (name) VALUES (%s)"
        mycursor.execute(query, (name,))
        
        # Commit the changes and close the connection
        mydb.commit()
        mydb.close()
        
        print("Name saved to the database.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

# Create the Tkinter window
root = tk.Tk()
root.title("Name Window")

# Tkinter widgets
label = tk.Label(root, text="Enter your name:")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=10)

button = tk.Button(root, text="Add Name", command=add_name)
button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()

