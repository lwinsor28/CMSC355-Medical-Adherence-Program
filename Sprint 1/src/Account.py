"""
Name: Account.py
Description: The account creation window.
"""

# Import shenanigans necessary to ensure cross-platform compatibility
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk


class SignupWindow:
    def __init__(self, database):
        # Open new window
        self.root = tk.Toplevel()

        # Database
        self.database = database

        # Instance variables defined in other functions
        self.main_frame = None
        self.left_frame = None
        self.right_frame = None

        # Account creation variables
        self.account_data = {
            "first_name": tk.StringVar(),
            "last_name": tk.StringVar(),
            "date_of_birth": tk.StringVar(),
            "username": tk.StringVar(),
            "password": tk.StringVar(),
            "email": tk.StringVar(),
            "phone_number": [tk.StringVar(), tk.StringVar(), tk.StringVar()],
        }

        # Grid constants
        self.TOP_ROW = 1
        self.COL_WIDTH = 3
        self.ROW_PADX = 5
        self.ROW_PADY = 5

        # Run all the functions that create the window
        self.init_root()
        self.init_frames()
        self.create_title_bar()
        self.create_left_column()
        self.create_right_column()
        self.create_create_account_button()

    def init_root(self):
        # Configure any window elements such as title, size, etc.

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
        # Configure the main frame
        self.main_frame = ttk.Frame(self.root, padding="3 3 12 12")
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
        # Show big title at the top of the window
        font = ('Magneto', 24)  # Goofy font bc why not
        tk.Label(self.main_frame, text="Create New Account", font=font).grid(
            column=0, row=0,
            columnspan=self.COL_WIDTH * 2, rowspan=1,
            padx=5, pady=0, sticky=(tk.N, tk.E, tk.W)
        )

    def create_left_column(self):
        # Load items in the left column

        # List that allows for an easy for loop to write out the whole left column.
        # For each individual element e, e[0] = display name, e[1] equivalent variable name for self.account_data
        items = (
            ("First Name", "first_name"),
            ("Date of Birth", "date_of_birth"),
            ("Username", "username"),
            ("Password", "password"),
            ("Email", "email"),
        )

        # Loop over items and put each item on screen with a label and text box
        for idx in range(len(items)):
            item = items[idx]

            tk.Label(self.left_frame, text=item[0]).grid(
                column=0, row=self.TOP_ROW + idx,
                columnspan=1, rowspan=1, padx=self.ROW_PADX, pady=self.ROW_PADX
            )
            self.account_data[item[1]] = tk.Entry(self.left_frame)
            self.account_data[item[1]].grid(
                column=1, row=self.TOP_ROW + idx,
                columnspan=5, rowspan=1, padx=self.ROW_PADX, pady=self.ROW_PADX,
                sticky="W"
            )

            # Enable password mode for the password box
            if item[1] == "password":
                self.account_data[item[1]]["show"] = "*"

        # Custom box layout for phone number
        # Initial label
        tk.Label(self.left_frame, text="Phone Number").grid(
            column=0, row=self.TOP_ROW + len(items),
            columnspan=1, rowspan=1, padx=0, pady=self.ROW_PADX
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
                columnspan=1, rowspan=1, padx=0, pady=self.ROW_PADX
            )
        # Generate text boxes
        phone_num_widths = (3, 3, 4)
        for idx in range(3):
            self.account_data["phone_number"][idx] = tk.Entry(
                phone_num_entry_frame, width=phone_num_widths[idx]
            )
            self.account_data["phone_number"][idx].grid(
                column=(idx * 2) + 0, row=0,
                columnspan=1, rowspan=1, padx=0, pady=self.ROW_PADX,
                sticky="W"
            )

    def create_right_column(self):
        # Load items in the right column

        # Last name
        tk.Label(self.right_frame, text="Last Name").grid(
            column=0, row=self.TOP_ROW + 0,
            columnspan=1, rowspan=1, padx=self.ROW_PADX, pady=self.ROW_PADX
        )
        self.account_data["last_name"] = tk.Entry(self.right_frame)
        self.account_data["last_name"].grid(
            column=1, row=self.TOP_ROW + 0,
            columnspan=2, rowspan=1, padx=self.ROW_PADX, pady=self.ROW_PADX,
            sticky="W"
        )

    def create_create_account_button(self):
        tk.Button(self.main_frame, text="Create Account").grid(
            column=1, row=2,
            columnspan=self.COL_WIDTH * 2, rowspan=1,
            padx=5, pady=0, sticky=(tk.N, tk.E, tk.W)
        )

class LoginWindow:
    def __init__(self):
        print("Not implemented yet")
