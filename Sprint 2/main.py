"""
Project: Medical Adherence Program
Class: CMSC 355-001 Fall 2024
Authors: Group 7
Assignment: Sprint 2
Date: 2024/11/15
"""

from src.App import App

# Import shenanigans necessary to ensure cross-platform compatibility
try:
    from tkinter import Tk
except ImportError:
    from Tkinter import Tk


if __name__ == '__main__':
    root = Tk()  # Root of application
    App(root)  # Load application with the root as, well, the root
    root.mainloop()  # Run until something says otherwise
