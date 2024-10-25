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

from src.Account import SignupWindow, LoginWindow
from src.Database import Database


class App:

    def __init__(self, main_root):
        # Root instance variable
        self.root = main_root

        # Instance variables assigned in other functions
        self.main_frame = None  # init_main_frame

        # Database
        self.database = Database()  # The original location of the loaded database

        # Load any necessary components
        self.init_root()
        self.init_main_frame()
        self.create_account_buttons()

    def init_root(self):
        # Configure any window elements such as title, size, etc.
        # Basically anything that isn't the *actual* application.

        self.root.title('Home: Medical Adherence Software - Group 7')  # Window title

        # Configure the root so that it does not interfere with the main_frame grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Window size
        self.root.geometry('400x300')

        # Window Logo
        logo = PhotoImage(file='./assets/medical_icon.png')
        self.root.iconphoto(False, logo)

    def init_main_frame(self):
        # Configure the main frame upon which sits most of the application
        self.main_frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.main_frame.grid(column=0, row=0, sticky=(N, S, E, W))

    def create_account_buttons(self):
        # Sign up button
        login_button = ttk.Button(self.main_frame, text="Sign Up", command=self.open_SignupWindow_with_db)
        login_button.grid(column=1, row=1)

        # Login button
        login_button = ttk.Button(self.main_frame, text="Login", command=LoginWindow)
        login_button.grid(column=2, row=1)

    def open_SignupWindow_with_db(self):
        # Tkinter is silly and old, so you can't pass arguments in button commands.
        # This helper function gets around that
        SignupWindow(self.database)

