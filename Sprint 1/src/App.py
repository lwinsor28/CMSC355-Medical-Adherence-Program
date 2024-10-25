"""
Name: App.py
Description: The main window of the program.
             All the Tkinter magic is initialized here and loaded in ../main.py
"""

# Import shenanigans necessary to ensure cross-platform compatibility
try:
    from tkinter import *
    from tkinter import ttk
except ImportError:
    from Tkinter import *
    import ttk

from src.Account import Account_Window


class App:

    def __init__(self, main_root):
        # Root instance variable
        self.root = main_root

        # Instance variables assigned in other functions
        self.main_frame = None

        # Load any necessary components
        self.init_root()
        self.init_main_frame()
        self.create_login_button()

    def init_root(self):
        # Configure any window elements such as title, size, etc.
        # Basically anything that isn't the *actual* application.

        self.root.title('Home: Medical Adherence Software - Group 7')  # Window title

        # Configure the root so it STAYS OUT THE WAY
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def init_main_frame(self):
        # Configure the main frame upon which sits most of the application
        self.main_frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.main_frame.grid(column=0, row=0, sticky=(N, S, E, W))

    def create_login_button(self):
        print("Creating login button")
        login_button = ttk.Button(self.main_frame, text="Login/Sign Up", command=Account_Window)
        login_button.grid(column=1, row=1)

