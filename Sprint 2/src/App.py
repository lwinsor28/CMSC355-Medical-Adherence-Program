"""
Name: App.py
Description: The main window of the program.
             All the Tkinter magic is initialized here and loaded in ../main.py
"""

# Import shenanigans necessary to ensure cross-platform compatibility
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import tkinter as tk
    import ttk

try:
    from src.Account import SignupWindow, LoginWindow
    from src.Alert import AlertWindow
    from src.Database import Database
    from src.Medication import MedicationMenuWindow
except ImportError:
    from Account import SignupWindow, LoginWindow
    from Alert import AlertWindow
    from Database import Database
    from Medication import MedicationMenuWindow
    quit()

NO_USER_MSG = "No User Signed In"


# FIXME: Add a database save for when the window is closed to ensure all work is saved.

class App:
    def __init__(self, main_root):
        # Root instance variable
        self.root = main_root

        # Grid constants
        self.TOP_ROW = 1

        # Instance variables assigned in other functions
        self.main_frame = None  # init_main_frame

        # Database
        self.database = Database()  # The original location of the loaded database
        self.database.load()
        self.current_user = tk.StringVar()  # Stores ID of signed-in user
        self.current_user.set(NO_USER_MSG)
        self.current_user_info = tk.StringVar()  # Stores a string that displays all user info to show who is logged in.
        self.current_user_info.set(NO_USER_MSG)

        # Load any necessary components
        self.init_root()
        self.init_main_frame()
        self.create_account_buttons()
        self.create_prescription_menu_button()
        self.create_current_user_label()

    def init_root(self):
        """Configure any window elements such as title, size, etc.
        Basically anything that isn't the *actual* application."""

        self.root.title('Home: Medical Adherence Software - Group 7')  # Window title

        # Configure the root so that it does not interfere with the main_frame grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Window size
        self.root.geometry('400x300')
        self.root.resizable(width=False, height=False)

        # Window Logo
        logo = tk.PhotoImage(file='./assets/medical_icon.png')
        self.root.iconphoto(False, logo)

    def init_main_frame(self):
        """Configure the main frame upon which sits most of the application"""
        self.main_frame = tk.Frame(self.root, padx=3, pady=5)
        self.main_frame.grid(column=0, row=0, sticky="NSEW")
        for col in range(1, 5):
            self.main_frame.columnconfigure(col, weight=1)

    def create_account_buttons(self):
        """Two buttons to open login and sign up windows."""
        # Sign up button
        login_button = ttk.Button(self.main_frame, text="Sign Up", command=self.click_sign_up_button)
        login_button.grid(column=1, row=self.TOP_ROW, columnspan=2,
                          padx=5, pady=5, sticky="NSEW")

        # Login button
        login_button = ttk.Button(self.main_frame, text="Login", command=self.click_log_in_button)
        login_button.grid(column=3, row=self.TOP_ROW, columnspan=2,
                          padx=5, pady=5, sticky="NSEW")

    def create_prescription_menu_button(self):
        """Button that opens the menu for managing prescriptions."""
        prescription_button = ttk.Button(self.main_frame, text="Manage Prescriptions",
                                         command=self.click_prescription_button)
        prescription_button.grid(column=1, row=self.TOP_ROW + 1, columnspan=2,
                                 padx=5, pady=5, sticky="NSEW")

    def create_current_user_label(self):
        """Temporary measure to make sure everything works. Jk, it will be here forever."""
        label_frame = tk.Frame(self.main_frame)
        label_frame.grid(column=1, row=self.TOP_ROW + 2, padx=5, pady=5, columnspan=4, sticky="NSEW")
        label_frame.columnconfigure(1, weight=1)
        label_frame.columnconfigure(2, weight=1)
        user_label1 = tk.Label(label_frame, text="Current User: ")
        user_label1.grid(column=1, row=1, sticky="NSE")
        user_label2 = tk.Label(label_frame, textvariable=self.current_user_info)
        user_label2.grid(column=2, row=1, columnspan=3, sticky="NSW")

    def click_sign_up_button(self):
        """Opens sign up menu and then updates the logged-in user label upon completion."""
        win = SignupWindow(self.database, self.current_user)
        win.root.bind("<Destroy>", self.account_action_finished)

    def click_log_in_button(self):
        """Opens login menu and then updates the logged-in user label upon completion."""
        win = LoginWindow(self.database, self.current_user)
        win.root.bind("<Destroy>", self.account_action_finished)

    def click_prescription_button(self):
        """Opens the prescription management menu"""
        win = MedicationMenuWindow(self.database, self.current_user)
        win.root.bind("<Destroy>", self.prescription_action_finished)

    def prescription_action_finished(self, e=None):
        """Runs when main prescription window is closed."""
        self.database.save_prescriptions()

    def account_action_finished(self, e=None):
        """Updates the label that displays the current user info. Also saves the customer database."""
        # Update user label
        user_info = str(self.database.get_customer_by_ID(self.current_user.get()))
        self.current_user_info.set(user_info)

        # Save customer database
        self.database.save_customers()
