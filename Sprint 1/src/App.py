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
    from src.Database import Database
except ImportError:
    print("Big problem boss. Imports ain't importing.")  # Hopefully impossible
    quit()

NO_USER_MSG = "No User Signed In"


class App:
    def __init__(self, main_root):
        # Root instance variable
        self.root = main_root

        # Instance variables assigned in other functions
        self.main_frame = None  # init_main_frame

        # Database
        self.database = Database()  # The original location of the loaded database
        self.current_user = tk.StringVar()  # Stores ID of signed-in user
        self.current_user.set(NO_USER_MSG)

        # Load any necessary components
        self.init_root()
        self.init_main_frame()
        self.create_account_buttons()
        self.create_current_user_label()

        self.load_database()

    def init_root(self):
        """Configure any window elements such as title, size, etc.
        # Basically anything that isn't the *actual* application."""

        self.root.title('Home: Medical Adherence Software - Group 7')  # Window title

        # Configure the root so that it does not interfere with the main_frame grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Window size
        self.root.geometry('400x300')

        # Window Logo
        logo = tk.PhotoImage(file='./assets/medical_icon.png')
        self.root.iconphoto(False, logo)

    def init_main_frame(self):
        """Configure the main frame upon which sits most of the application"""
        self.main_frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.main_frame.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(3, weight=1)

    def create_account_buttons(self):
        # Sign up button
        login_button = ttk.Button(self.main_frame, text="Sign Up", command=self.click_sign_up_button)
        login_button.grid(column=1, row=1, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Login button
        login_button = ttk.Button(self.main_frame, text="Login", command=self.click_log_in_button)
        login_button.grid(column=3, row=1, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))

    def create_current_user_label(self):
        """Temporary measure to make sure everything works"""
        label_frame = tk.Frame(self.main_frame)
        label_frame.grid(column=1, row=2, padx=5, pady=5, columnspan=4, sticky=(tk.N, tk.S, tk.E, tk.W))
        label_frame.columnconfigure(1, weight=1)
        label_frame.columnconfigure(2, weight=1)
        user_label1 = tk.Label(label_frame, text="Current User: ")
        user_label1.grid(column=1, row=1, sticky=(tk.N, tk.S, tk.E))
        user_label2 = tk.Label(label_frame, textvariable=self.current_user)
        user_label2.grid(column=2, row=1, columnspan=3, sticky=(tk.N, tk.S, tk.W))

    def click_sign_up_button(self):
        """Tkinter is silly and old, so you can't pass arguments in button commands.
        This helper function gets around that"""
        SignupWindow(self.database, self.current_user)

    def click_log_in_button(self):
        LoginWindow(self.database, self.current_user)

    def load_database(self):
        """Loads previous database. Otherwise, loads in defaults."""
        try:
            self.database.load()
        except:
            print("Problem loading database. Creating new database and inserting defaults...")
            # No file was loaded. Let's load some defaults!
            from datetime import date
            # Default users
            self.database.add_customer("Satoru", "Gojo", "thestr0ngest", "hollow&purple1989",
                                       "satorugojo@jjhs.edu", "5551234567", date.fromisoformat("1989-12-07"))
            self.database.add_customer("Sukuna", "Ryoumen", "kingofcurses", "20fingers",
                                       "imhim@malevolentshrine.lol", "5556666666",
                                       date.fromisoformat("2018-06-01"))
            # Save
            self.database.save_all()
