"""
Name: App.py
Description: The main window of the program.
             All the Tkinter magic is initialized here and loaded in ../main.py
"""

# Import shenanigans necessary to ensure cross-platform compatibility
try:
    from tkinter import Tk
except ImportError:
    from Tkinter import Tk


class App:

    def __init__(self, main_root):
        # Root instance variable
        self.root = main_root

        # Load any necessary components
        load_configuration()

    def load_configuration(self):
        # Configure any window elements such as title, size, etc.
        # Basically anything that isn't the *actual* application.
        self.root.title('Medical Adherence Software - Group 7')
