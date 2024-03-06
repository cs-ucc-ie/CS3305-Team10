import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue
import subprocess
import new_avg


class IndexPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Index Page")

        # Create and configure the notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Add the Add Name page
        add_name_page = AddNamePage(self.notebook)
        self.notebook.add(add_name_page, text="Add Name")

        # Add the Engagement Graph page
        graph_page = GraphPage(self.notebook)
        self.notebook.add(graph_page, text="Engagement Graph")


class AddNamePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        label = tk.Label(self, text="This is the Add Name Page")
        label.pack(pady=20)

        button = tk.Button(self, text="Add name", command=self.run_name)
        button.pack()

    def run_name(self):
        # Execute the facial expression recognition code using subprocess asynchronously
        subprocess.Popen(["python", "add_name.py"])


class GraphPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.data_queue = Queue()
        self.x_data = []  # Initialize x_data to store time intervals
        self.y_data = []  # Initialize y_data to store engagement levels
        self.facial_recognition_process = None

        label = tk.Label(self, text="Engagement Graph")
        label.pack(pady=20)

        # Label to display average engagement level
        self.avg_label = tk.Label(self, text="Average Engagement Level: ")
        self.avg_label.pack()

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(expand=True, fill="both")

        # Create button for starting facial recognition
        self.start_button = tk.Button(self, text="Start Facial Recognition", command=self.start_facial_recognition)
        self.start_button.pack()

        # Update the graph continuously with new data points
        self.update_from_queue()

    def update_graph(self):
        self.ax.clear()

        # Plot the data on the graph
        for i in self.y_data:
            if i > 50:
                self.ax.plot(self.x_data, self.y_data, marker='o', linestyle='-', color='g')
            else:
                self.ax.plot(self.x_data, self.y_data, marker='o', linestyle='-', color='r')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Engagement Level')
        self.ax.set_title('Engagement Level Over Time')
        self.fig.tight_layout()

        # Draw canvas
        self.canvas.draw()

    def start_facial_recognition(self):
        # Start the facial recognition process in a separate process
        if self.facial_recognition_process is None:
            self.facial_recognition_process = Process(target=new_avg.facial_recognition, args=(self.data_queue,))
            self.facial_recognition_process.start()

            # Disable the button after starting the process
            self.start_button.config(state=tk.DISABLED)

    def update_from_queue(self):
        if self.facial_recognition_process is None:
            # Enable the button if the process is not running
            self.start_button.config(state=tk.NORMAL)

        # Update the graph with new data points from the queue
        while not self.data_queue.empty():
            data_point = self.data_queue.get()
            self.y_data.append(data_point)
            self.x_data.append(len(self.y_data))  # Use the length of y_data as x-coordinate

        self.update_graph()

        # Calculate and display the average engagement level
        if self.y_data:
            average_engagement = sum(self.y_data) / len(self.y_data)
            self.avg_label.config(text=f"Average Engagement Level: {int(average_engagement):.2f}%")

        # Schedule the next update after 1 second
        self.after(1000, self.update_from_queue)


if __name__ == "__main__":
    app = IndexPage()
    app.mainloop()

