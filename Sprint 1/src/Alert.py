"""
Name: Alert.py
Description: When called, this shows a popup window with a message.
             This is mostly used to tell users when there is an issue with some input.
"""

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk


class AlertWindow:
    def __init__(self, message):
        # Open new window
        self.root = tk.Toplevel()

        # Alert message
        self.MESSAGE = tk.StringVar()
        self.MESSAGE.set(message)

        self.main_frame = None

        self.init_root()
        self.init_main_frame()
        self.init_label()

    def init_root(self):
        """Configure any window elements such as title, size, etc.
        Basically anything that isn't the *actual* window."""

        self.root.title('Alert: Medical Adherence Software - Group 7')  # Window title

        # Configure the root so that it does not interfere with the main_frame grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Window size
        self.root.geometry('500x150')

        # Window Logo
        logo = tk.PhotoImage(file='./assets/medical_icon.png')
        self.root.iconphoto(False, logo)

    def init_main_frame(self):
        """Configure the main frame upon which sits most of the application"""
        self.main_frame = tk.Frame(self.root, padx=3, pady=12)
        self.main_frame.grid(column=0, row=0, sticky="NSEW")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

    def init_label(self):
        """Slap the label and exit button on there! Real simple stuff"""
        label = tk.Label(self.main_frame, textvariable=self.MESSAGE)
        label.grid(column=0, row=0, sticky="NSEW")

        button = tk.Button(self.main_frame, text="Okay", command=self.exit)
        button.grid(column=0, row=1, pady=15, sticky="N")

    def exit(self):
        self.root.destroy()
