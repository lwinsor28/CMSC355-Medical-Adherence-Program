"""
Name: account_window.py
Description: The login/account creation window.
"""

# Import shenanigans necessary to ensure cross-platform compatibility
try:
    from tkinter import Tk
    from tkinter import ttk
except ImportError:
    from Tkinter import Tk
    import ttk


class Account_Window:
    def __init__(self, anchor_frame):
        self.root = anchor_frame

        self.init_root()

    def init_root(self):
        # Configure any window elements such as title, size, etc.

        self.root.title('Account Management: Medical Adherence Software - Group 7')  # Window title

        # Configure the root so it STAYS OUT THE WAY
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
