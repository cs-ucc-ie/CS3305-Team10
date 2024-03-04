import tkinter as tk
from tkinter import ttk
import os
import subprocess

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

        # Add the Facial Expression Recognition page
        facial_expr_recognition_page = FacialExprRecognitionPage(self.notebook)
        self.notebook.add(facial_expr_recognition_page, text="Facial Expression Recognition")

class AddNamePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        label = tk.Label(self, text="This is the Add Name Page")
        label.pack(pady=20)

        button = tk.Button(self, text="Add name", command=self.run_name)
        button.pack()

        button = tk.Button(self, text="Next", command=self.navigate_to_facial_expr_recognition)
        button.pack()
    def run_name(self):

        # Execute the facial expression recognition code using subprocess
        subprocess.run(["python", "add_name.py"])

        # After executing, navigate back to the Add Name page
        self.navigate_to_add_name()

    def navigate_to_add_name(self):
        self.master.select(0)  # Switch to the Add Name page

    def navigate_to_facial_expr_recognition(self):
        self.master.select(1)  # Switch to the Facial Expression Recognition page

class FacialExprRecognitionPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        label = tk.Label(self, text="This is the Facial Expression Recognition Page")
        label.pack(pady=20)

        button = tk.Button(self, text="Run Facial Expression Recognition", command=self.run_facial_expr_recognition)
        button.pack()

        back_button = tk.Button(self, text="Back to Add Name", command=self.navigate_to_add_name)
        back_button.pack()

    def run_facial_expr_recognition(self):

        # Execute the facial expression recognition code using subprocess
        subprocess.run(["python", "new_avg.py"])

        # After executing, navigate back to the Add Name page
        self.navigate_to_add_name()

    def navigate_to_add_name(self):
        self.master.select(0)  # Switch to the Add Name page

if __name__ == "__main__":
    app = IndexPage()
    app.mainloop()

