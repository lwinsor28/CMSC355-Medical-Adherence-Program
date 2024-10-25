"""
Name: Account.py
Description: The login/account creation window.
"""

# Import shenanigans necessary to ensure cross-platform compatibility
try:
    from tkinter import *
    from tkinter import ttk
except ImportError:
    from Tkinter import *
    import ttk


class Account_Window:
    def __init__(self):
        # Open new window
        self.root = Toplevel()

        # Instance variables defined in other functions
        self.main_frame = None

        self.init_root()
        self.init_main_frame()

    def init_root(self):
        # Configure any window elements such as title, size, etc.

        self.root.title('Account Management: Medical Adherence Software - Group 7')  # Window title

        # Configure the root so it STAYS OUT THE WAY
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def init_main_frame(self):
        # Configure the main frame of the window
        self.main_frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.main_frame.grid(column=0, row=0, sticky=(N, S, E, W))
