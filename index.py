import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue
import subprocess
import new_avg

# Import modules from add_name.py
from add_name import add_name

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------

selectionbar_color = '#ffffff'
sidebar_color = '#91BDD2'
header_color = '#91BDD2'
visualisation_frame_color = "#ffffff"

# ------------------------ MULTIPAGE FRAMES ------------------------------------

# GRAPH
class Frame1(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Engagement Graph', font=("Arial", 15))
        label.pack(pady=20)

        self.data_queue = Queue()
        self.x_data = []  # Initialize x_data to store time intervals
        self.y_data = []  # Initialize y_data to store engagement levels
        self.facial_recognition_process = None

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(expand=True, fill="both")

        # Create button for starting facial recognition
        self.start_button = tk.Button(command=lambda: self.start_facial_recognition())
        # Add button for adding a name
        #self.add_name_button = tk.Button(self, text="Add Name", command=add_name)
        #self.add_name_button.pack()

        # Label to display average engagement level
        self.avg_label = tk.Label(self, text="Average Engagement Level: ")
        self.avg_label.pack()

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

            # Update the graph continuously with new data points
            self.update_from_queue()

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

# ----------------------------- CUSTOM WIDGETS ---------------------------------

class SidebarSubMenu(tk.Frame):
    """
    A submenu which can have multiple options and these can be linked with
    functions.
    """

    def __init__(self, parent, sub_menu_heading, sub_menu_options):
        """
        parent: The frame where submenu is to be placed
        sub_menu_heading: Heading for the options provided
        sub_menu_operations: Options to be included in sub_menu
        """
        tk.Frame.__init__(self, parent)
        self.config(bg=sidebar_color)
        self.sub_menu_heading_label = tk.Label(self,
                                               text=sub_menu_heading,
                                               bg=sidebar_color,
                                               fg="#333333",
                                               font=("Arial", 10)
                                               )
        self.sub_menu_heading_label.place(x=30, y=10, anchor="w")

        sub_menu_sep = ttk.Separator(self, orient='horizontal')
        sub_menu_sep.place(x=30, y=30, relwidth=0.8, anchor="w")

        self.options = {}
        for n, x in enumerate(sub_menu_options):
            self.options[x] = tk.Button(self,
                                        text=x,
                                        bg=sidebar_color,
                                        font=("Arial", 9, "bold"),
                                        bd=0,
                                        cursor='hand2',
                                        activebackground='#ffffff',
                                        )
            self.options[x].place(x=30, y=45 * (n + 1), anchor="w")

class TkinterApp(tk.Tk):
    """
     The class creates a header and sidebar for the application. Also creates
     two submenus in the sidebar, one for attendance overview with options to
     track students and modules, view poor attendance and another for
     database management, with options to update and add new modules to the
     database.
    """

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("eMOTIONS")

        # ------------- BASIC APP LAYOUT -----------------

        self.geometry("1100x700")
        self.resizable(0, 0)
        self.title('eMOTIONS')
        self.config(background=selectionbar_color)
        icon = tk.PhotoImage(file='logo.png')
        self.iconphoto(True, icon)

        # ---------------- HEADER ------------------------

        self.header = tk.Frame(self, bg=header_color)
        self.header.place(relx=0.3, rely=0, relwidth=0.7, relheight=0.1)

        # ---------------- SIDEBAR -----------------------
        # CREATING FRAME FOR SIDEBAR
        self.sidebar = tk.Frame(self, bg=sidebar_color)
        self.sidebar.place(relx=0, rely=0, relwidth=0.3, relheight=1)

        # UNIVERSITY LOGO AND NAME
        self.brand_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.brand_frame.place(relx=0, rely=0, relwidth=1, relheight=0.35)
        self.uni_logo = icon.subsample(9)
        logo = tk.Label(self.brand_frame, image=self.uni_logo, bg=sidebar_color)
        logo.place(x=5, y=20)

        uni_name = tk.Label(self.brand_frame,
                            text='eMOTIONS',
                            bg=sidebar_color,
                            font=("", 15, "bold")
                            )
        uni_name.place(x=200, y=27, anchor="w")

        # SUBMENUS IN SIDE BAR

        # # SUBMENU 1
        self.submenu_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.submenu_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.85)
        submenu1 = SidebarSubMenu(self.submenu_frame,
                                  sub_menu_heading='MENU',
                                  sub_menu_options=["Run application"],
                                  )
        submenu1.options["Run application"].config(
        command=lambda: self.frames[Frame1].start_facial_recognition()
        )

        submenu1.place(relx=0, rely=0.025, relwidth=1, relheight=0.3)

        # --------------------  MULTI PAGE SETTINGS ----------------------------

        container = tk.Frame(self)
        container.config(highlightbackground="#808080", highlightthickness=0.5)
        container.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)

        self.frames = {}

        for F in (Frame1,):

            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame(Frame1)

    def show_frame(self, cont):
        """
        The function 'show_frame' is used to raise a specific frame (page) in
        the tkinter application and update the title displayed in the header.

        Parameters:
        cont (str): The name of the frame/page to be displayed.
        title (str): The title to be displayed in the header of the application.

        Returns:
        None
        """
        frame = self.frames[cont]
        frame.tkraise()

    def add_name_window(self):
        """
        Function to open the window for adding a name.
        """
        root = tk.Tk()
        root.title("Name Window")

        label = tk.Label(root, text="Enter your name:")
        label.pack(pady=10)

        entry = tk.Entry(root)
        entry.pack(pady=10)

        button = tk.Button(root, text="Add Name", command=lambda: add_name(entry.get()))
        button.pack(pady=10)

        #root.mainloop()


if __name__ == "__main__":
    app = TkinterApp()
    app.mainloop()