"""
Name: Medication.py
Description: Holds the windows that are brought up from the "Manage Prescription" button on the main screen.
"""

# Import shenanigans necessary to ensure cross-platform compatibility
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

try:
    from src.Validator import Validator
except ImportError:
    from Validator import Validator

TITLE_FONT = ('Magneto', 24)  # Goofy font bc why not

class MedicationMenuWindow:
    """Shows the main screen [PRO01] with the options for managing prescriptions shown and nothing else."""
    def __init__(self, database, current_user):
        # Open new window
        self.root = tk.Toplevel()

        # Database
        self.database = database
        self.current_user = current_user

        # Frames defined in other functions
        self.main_frame = None
        self.button_frame = None

        # Grid constants
        #self.TOP_ROW = 1
        self.COL_WIDTH = 3
        #self.ROW_PADX = 5
        #self.ROW_PADY = 10

        # Colors
        self.DARK_GREY = "#b3b3b3"

        # Run all the functions that create the window
        self.init_root()
        self.init_frames()
        self.create_title_bar()

    def init_root(self):
        """Configure any window elements such as title, size, etc."""

        self.root.title('Prescriptions: Medical Adherence Software - Group 7')  # Window title

        # Configure the root so that it does not interfere with the main_frame grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Window size
        self.root.geometry('450x150')
        self.root.resizable(width=False, height=False)

        # Window Logo
        logo = tk.PhotoImage(file='./assets/medical_icon.png')
        self.root.iconphoto(False, logo)

    def init_frames(self):
        """Configure the main and button frames."""
        # Main frame
        self.main_frame = tk.Frame(self.root, padx=3, pady=5)
        self.main_frame.grid(column=0, row=0, sticky="NSEW")

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Button frame
        self.button_frame = tk.Frame(self.root, padx=3, pady=5)
        self.main_frame.grid(column=0, row=0, sticky="NSEW")

    def create_title_bar(self):
        """Show header text."""
        tk.Label(self.main_frame, text="Manage Prescriptions", font=TITLE_FONT, background=self.DARK_GREY).grid(
            column=0, row=0,
            columnspan=self.COL_WIDTH * 2, rowspan=1,
            padx=5, pady=0, sticky="NEW"
        )

    def create_buttons(self):
        """Create the three option buttons to select which prescription operation to execute."""
        pass
