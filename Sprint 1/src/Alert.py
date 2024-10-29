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
    def __init__(self):
        # Open new window
        self.root = tk.Toplevel()
