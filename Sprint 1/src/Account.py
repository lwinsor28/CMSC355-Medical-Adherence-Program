"""
Name: Account.py
Description: The account creation and login windows are loaded from here.
"""

# Import shenanigans necessary to ensure cross-platform compatibility
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk
from datetime import date

try:
    from src.Validator import Validator
except ImportError:
    from Validator import Validator

TITLE_FONT = ('Magneto', 24)  # Goofy font bc why not


class SignupWindow:
    def __init__(self, database, current_user):
        # Open new window
        self.root = tk.Toplevel()

        # Database
        self.database = database
        self.current_user = current_user

        # Frames defined in other functions
        self.main_frame = None
        self.left_frame = None
        self.right_frame = None

        # Account creation variables
        self.account_data = {
            "first_name": tk.Entry(),
            "last_name": tk.Entry(),
            "date_of_birth": tk.Entry(),
            "username": tk.Entry(),
            "password": tk.Entry(),
            "email": tk.Entry(),
            "phone_number": [tk.Entry(), tk.Entry(), tk.Entry()],
        }

        # Grid constants
        self.TOP_ROW = 1
        self.COL_WIDTH = 3
        self.ROW_PADX = 5
        self.ROW_PADY = 5

        # Colors
        self.DARK_GREY = "#b3b3b3"
        self.LIGHT_GREY = "#e6e6e6"

        # Run all the functions that create the window
        self.init_root()
        self.init_frames()
        self.create_title_bar()
        self.create_left_column()
        self.create_right_column()
        self.create_create_account_button()

    def init_root(self):
        """Configure any window elements such as title, size, etc."""

        self.root.title('Account Creation: Medical Adherence Software - Group 7')  # Window title

        # Configure the root so that it does not interfere with the main_frame grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Window size
        self.root.geometry('450x300')
        self.root.resizable(width=False, height=False)

        # Window Logo
        logo = tk.PhotoImage(file='./assets/medical_icon.png')
        self.root.iconphoto(False, logo)

    def init_frames(self):
        """Configure the main content frames of the window."""
        # Configure the main frame
        self.main_frame = tk.Frame(self.root, padx=3, pady=5)
        self.main_frame.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Allow frames within main frame to expand and fill space
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        # Configure the left column frame
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W),
                             columnspan=1)
        self.left_frame.columnconfigure(1, weight=3)
        self.left_frame.columnconfigure(0, weight=1)

        # Configure the right column frame
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.grid(column=1, row=1, sticky=(tk.N, tk.S, tk.E, tk.W),
                              columnspan=1)
        self.right_frame.columnconfigure(1, weight=1)
        self.right_frame.columnconfigure(0, weight=2)

    def create_title_bar(self):
        """Show big title at the top of the window"""
        font = ('Magneto', 24)  # Goofy font bc why not
        tk.Label(self.main_frame, text="Create New Account", font=TITLE_FONT, background=self.DARK_GREY).grid(
            column=0, row=0,
            columnspan=self.COL_WIDTH * 2, rowspan=1,
            padx=5, pady=0, sticky=(tk.N, tk.E, tk.W)
        )

    def create_left_column(self):
        """Load items in the left column"""

        # List that allows for an easy for loop to write out the whole left column.
        # For each individual element e, e[0] = display name, e[1] equivalent variable name for self.account_data
        items = (
            ("First Name", "first_name"),
            ("Username", "username"),
            ("Password", "password"),
            ("Email", "email"),
        )

        # Loop over items and put each item on screen with a label and text box
        for idx in range(len(items)):
            item = items[idx]

            tk.Label(self.left_frame, text=item[0]).grid(
                column=0, row=self.TOP_ROW + idx,
                columnspan=1, rowspan=1, padx=self.ROW_PADX, pady=self.ROW_PADY
            )
            self.account_data[item[1]] = tk.Entry(self.left_frame)
            self.account_data[item[1]].grid(
                column=1, row=self.TOP_ROW + idx,
                columnspan=5, rowspan=1, padx=self.ROW_PADX, pady=self.ROW_PADY,
                sticky="W"
            )

            # Enable password mode for the password box
            if item[1] == "password":
                self.account_data[item[1]]["show"] = "*"

        # Custom box layout for phone number
        # Initial label
        tk.Label(self.left_frame, text="Phone Number").grid(
            column=0, row=self.TOP_ROW + len(items),
            columnspan=1, rowspan=1, padx=0, pady=self.ROW_PADY
        )
        # It gets its own frame to not ruin the other rows with its complexity
        phone_num_entry_frame = tk.Frame(self.left_frame)
        phone_num_entry_frame.grid(
            column=1, row=self.TOP_ROW + len(items),
            columnspan=1, rowspan=1, padx=self.ROW_PADX, pady=self.ROW_PADY,
            sticky="W"
        )
        # Generate labels
        phone_num_labels = ("-", "-")
        for idx in range(len(phone_num_labels)):
            tk.Label(phone_num_entry_frame, text=phone_num_labels[idx]).grid(
                column=(idx * 2) + 1, row=0,
                columnspan=1, rowspan=1, padx=0, pady=self.ROW_PADY
            )
        # Generate text boxes
        phone_num_widths = (3, 3, 4)
        for idx in range(3):
            self.account_data["phone_number"][idx] = tk.Entry(
                phone_num_entry_frame, width=phone_num_widths[idx]
            )
            self.account_data["phone_number"][idx].grid(
                column=(idx * 2) + 0, row=0,
                columnspan=1, rowspan=1, padx=0, pady=self.ROW_PADY,
                sticky="W"
            )

    def create_right_column(self):
        """Load items in the right column"""

        # Last name
        tk.Label(self.right_frame, text="Last Name").grid(
            column=0, row=self.TOP_ROW + 0,
            columnspan=1, rowspan=1, padx=self.ROW_PADX, pady=self.ROW_PADY
        )
        self.account_data["last_name"] = tk.Entry(self.right_frame)
        self.account_data["last_name"].grid(
            column=1, row=self.TOP_ROW + 0,
            columnspan=2, rowspan=1, padx=self.ROW_PADX, pady=self.ROW_PADY,
            sticky="W"
        )

    def create_create_account_button(self):
        tk.Button(self.main_frame, text="Create Account", command=self.click_create_account_button).grid(
            column=1, row=2,
            columnspan=self.COL_WIDTH * 2, rowspan=1,
            padx=5, pady=0, sticky=(tk.N, tk.E, tk.W)
        )

    def click_create_account_button(self):
        """Adds new account to database and closes the window.
        Checks to make sure no issues exist with user input"""

        # Validation checks
        validator = Validator()
        validator.check_username_does_not_exist(self.account_data["username"].get(), self.database)  # TC02
        validator.check_valid_email_format(self.account_data["email"].get())  # TC03
        validator.check_valid_password_format(self.account_data["password"].get())  # TC04

        # Check that no validation checks failed
        if validator.no_failures():
            new_ID = self.database.add_customer(
                self.account_data["first_name"].get(),
                self.account_data["last_name"].get(),
                self.account_data["username"].get(),
                self.account_data["password"].get(),
                self.account_data["email"].get(),
                self.account_data["phone_number"][0].get() +
                self.account_data["phone_number"][1].get() +
                self.account_data["phone_number"][2].get(),
            )
            self.current_user.set(str(self.database.get_customer_by_ID(new_ID)))
            # self.current_user.set(new_ID) Ideally should store just ID, but this is temporary
            self.database.save_customers()
            self.root.destroy()

        # Validation checks failed, show errors
        else:
            validator.display_failures()


class LoginWindow:
    def __init__(self, database, current_user):
        # Open new window
        self.root = tk.Toplevel()

        # Database
        self.database = database
        self.current_user = current_user

        # Frames defined in other functions
        self.main_frame = None

        # Account creation variables
        self.account_data = {
            "username": tk.StringVar(),
            "password": tk.StringVar(),
        }

        # Grid constants
        self.TOP_ROW = 1
        self.COL_WIDTH = 3
        self.ROW_PADX = 5
        self.ROW_PADY = 10

        # Colors
        self.DARK_GREY = "#b3b3b3"

        # Run all the functions that create the window
        self.init_root()
        self.init_frames()
        self.create_title_bar()
        self.create_login_entries()
        self.create_login_button()

    def init_root(self):
        """Configure any window elements such as title, size, etc."""

        self.root.title('Login: Medical Adherence Software - Group 7')  # Window title

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
        """Configure the main frame"""
        self.main_frame = tk.Frame(self.root, padx=3, pady=5)
        self.main_frame.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Allow columns to fill space
        for col in range(self.COL_WIDTH * 2):
            self.main_frame.columnconfigure(col, weight=1)

        # Login button fills vertical space
        self.main_frame.rowconfigure(self.TOP_ROW + 1, weight=1)

    def create_title_bar(self):
        """Show big title at the top of the window"""
        tk.Label(self.main_frame, text="Login", font=TITLE_FONT, background=self.DARK_GREY).grid(
            column=0, row=self.TOP_ROW - 1,
            columnspan=self.COL_WIDTH * 2, rowspan=1,
            padx=5, pady=0, sticky=(tk.N, tk.E, tk.W)
        )

    def create_login_entries(self):
        """Create labels and entries for login information"""
        items = (
            ("Username:", "username"),
            ("Password:", "password")
        )

        for idx in range(len(items)):
            item = items[idx]
            tk.Label(self.main_frame, text=item[0]).grid(
                column=idx * self.COL_WIDTH, row=self.TOP_ROW + 0,
                columnspan=1, rowspan=1, padx=self.ROW_PADX, pady=self.ROW_PADY
            )
            self.account_data[item[1]] = tk.Entry(self.main_frame)
            self.account_data[item[1]].grid(
                column=(idx * self.COL_WIDTH) + 1, row=self.TOP_ROW + 0,
                columnspan=2, rowspan=1, padx=self.ROW_PADX, pady=self.ROW_PADY,
                sticky="W"
            )

            # Enable password mode for the password box
            if item[1] == "password":
                self.account_data[item[1]]["show"] = "*"

    def create_login_button(self):
        tk.Button(self.main_frame, text="Login", command=self.click_login_button).grid(
            column=4, row=self.TOP_ROW + 1,
            columnspan=2, rowspan=2,
            padx=5, pady=5, sticky=(tk.S, tk.E, tk.W)
        )

    def click_login_button(self):
        """Find user that matches username and password, then set them as active user.
        If issues arise, show an alert popup that explain what went wrong"""

        username = self.account_data["username"].get()
        password = self.account_data["password"].get()

        # Run validation checks
        validator = Validator()
        validator.check_username_exists(username, self.database)  # TC06
        validator.check_username_password_match(username, password, self.database)  # TC07

        # Continue with login process if no validation failures occured
        if validator.no_failures():
            # Get user date corresponding with username and password
            result = self.database.get_customer_by_username_password(
                self.account_data["username"].get(),
                self.account_data["password"].get()
            )

            # If somehow there is no valid user even after validation passed
            if result is None:
                self.current_user.set("Error: No User Found")
            else:
                self.current_user.set(str(self.database.get_customer_by_ID(result.ID)))
                # self.current_user.set(result.ID)
                """Ideally the above should store just ID, but this is temporary.
                Right now it stores the whole customer object cast to a string so that it can display all information
                on the main page"""

            self.root.destroy()

        # Validation failed, display the messages
        else:
            validator.display_failures()
