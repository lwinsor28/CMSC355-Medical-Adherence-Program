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

        # Grid constants
        self.TOP_ROW = 1
        self.COL_WIDTH = 3

        # Colors
        self.DARK_GREY = "#b3b3b3"

        # Run all the functions that create the window
        self.init_root()
        self.init_frames()
        self.create_title_bar()
        self.create_buttons()

    def init_root(self):
        """Configure any window elements such as title, size, etc."""

        self.root.title('Prescriptions: Medical Adherence Software - Group 7')  # Window title

        # Configure the root so that it does not interfere with the main_frame grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Window size
        self.root.geometry('450x150')
        self.root.resizable(width=True, height=True)

        # Window Logo
        logo = tk.PhotoImage(file='./assets/medical_icon.png')
        self.root.iconphoto(False, logo)

    def init_frames(self):
        """Configure the main and button frames."""
        # Main frame
        self.main_frame = tk.Frame(self.root, padx=3, pady=5)
        self.main_frame.grid(column=0, row=0, sticky="NSEW")

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=1)
        self.main_frame.rowconfigure(self.TOP_ROW, weight=1)

    def create_title_bar(self):
        """Show header text."""
        tk.Label(self.main_frame, text="Manage Prescriptions", font=TITLE_FONT, background=self.DARK_GREY).grid(
            column=0, row=0,
            columnspan=self.COL_WIDTH * 2, rowspan=1,
            padx=5, pady=0, sticky="NEW"
        )

    def create_buttons(self):
        """Create the three option buttons to select which prescription operation to execute."""
        buttonContents = (
            ("Add Prescription", self.click_add_prescription),
            ("Edit Prescriptions", self.click_edit_prescriptions),
            ("Delete Prescriptions", self.click_delete_prescriptions)
        )

        for idx in range(len(buttonContents)):
            ttk.Button(self.main_frame, text=buttonContents[idx][0], command=buttonContents[idx][1]).grid(
                column=idx, row=self.TOP_ROW, sticky="NSEW", padx=5, pady=5, rowspan=2
            )

    def click_add_prescription(self):
        win = AddMedicationWindow("Add Prescription", self.database, self.current_user)
        win.root.bind("<Destroy>", self.option_window_close)

    def click_edit_prescriptions(self):
        win = EditMedicationWindow("Edit Prescription", self.database, self.current_user)
        win.root.bind("<Destroy>", self.option_window_close)

    def click_delete_prescriptions(self):
        win = DeleteMedicationWindow(self.database, self.current_user)
        win.root.bind("<Destroy>", self.option_window_close)

    def option_window_close(self, e=None):
        """Runs when any of the prescription option windows close."""
        self.database.save_prescriptions()
        self.root.focus()


class _MedicationInputParent:
    """Since the add and edit prescription windows are very nearly identical, this parent class implements
    the shared input boxes, window configuration, etc. for both and is used as a superclass.

    The inheriting classes need only implement the differences. Namely, if prescriptions are
    named (add) or selected (edit), and what changes in the database when the Done button is clicked.

    Note: Row 1 (self.TOP_ROW) is reserved for the name of prescription box implemented by the child."""

    def __init__(self, window_title, done_func, database, current_user, drug_name_immutable=False):
        # Open new window
        self.root = tk.Toplevel()
        self.title = tk.StringVar()
        self.title.set(window_title)

        # Which function to execute when the Done button is clicked
        self.done_func = done_func
        self.done_button = None
        # Flags drug name field to be blocked from editing (off by default)
        self.drug_name_immutable = drug_name_immutable

        # Database
        self.database = database
        self.current_user = current_user

        # Frames defined in other functions
        self.main_frame = None

        # Holds all fields except for name of prescription (implemented by child).
        self.prescription_data = {
            "drug_name": tk.StringVar(),
            "doctor": tk.StringVar(),
            "date_issued": (tk.StringVar(), tk.StringVar(), tk.StringVar()),
            "dosage": tk.StringVar(),
            "time_btwn_dose": tk.StringVar(),
            "expiration_date": (tk.StringVar(), tk.StringVar(), tk.StringVar()),
            "side_effects": tk.StringVar()
        }

        # Grid constants
        self.TOP_ROW = 2
        self.COL_WIDTH = 4

        # Colors
        self.DARK_GREY = "#b3b3b3"

        # Duration modifiers (for prescription_data.time_btwn_dose)
        self.duration_mods = [
            ["seconds", "minutes", "hours", "days", "weeks"],  # modifier names
            [1, 60, 3600, 86400, 604800]  # seconds per mod
        ]
        self.selected_duration_mod = tk.StringVar()
        self.selected_duration_mod.set(self.duration_mods[0][3])

        # Run all the functions that create the window
        self.init_root()
        self.init_frames()
        self.create_title_bar()
        self.create_shared_elements()

        # Event bindings
        self.root.bind("<KeyPress-Return>", self.done_func)

    def init_root(self):
        """Configure any window elements such as title, size, etc."""

        self.root.title(f'{self.title.get()}: Medical Adherence Software - Group 7')  # Window title

        # Configure the root so that it does not interfere with the main_frame grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Window size
        self.root.geometry('450x330')
        self.root.resizable(width=True, height=True)

        # Window Logo
        logo = tk.PhotoImage(file='./assets/medical_icon.png')
        self.root.iconphoto(False, logo)

    def init_frames(self):
        """Configure the main and button frames."""
        # Main frame
        self.main_frame = tk.Frame(self.root, padx=3, pady=5)
        self.main_frame.grid(column=0, row=0, sticky="NSEW")

        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

    def create_title_bar(self):
        """Creates a header with the text from self.title"""
        tk.Label(self.main_frame, textvariable=self.title, font=TITLE_FONT, background=self.DARK_GREY).grid(
            column=0, row=self.TOP_ROW - 2,
            columnspan=self.COL_WIDTH, rowspan=1,
            padx=5, pady=0, sticky="NEW"
        )

    def create_shared_elements(self):
        """Create all shared elements except for the name of the prescription."""
        # Holds the names and their related self.prescription_data references for text entry widgets
        # [0] = prescription_data name, [1] = display name
        items = (
            ("drug_name", "Prescription Name"),
            ("doctor", "Name of Prescriber"),
            ("dosage", "Dosage"),
            ("side_effects", "Side Effects")
        )

        date_items = (
            ("date_issued", "Date Issued"),
            ("expiration_date", "Expiration Date")
        )

        # Create entry boxes
        for idx in range(len(items)):
            item = items[idx]

            tk.Label(self.main_frame, text=item[1]).grid(
                column=0, row=self.TOP_ROW + idx + 1,
                columnspan=1, sticky="NSEW", padx=5, pady=5
            )
            entryBox = tk.Entry(self.main_frame, textvariable=self.prescription_data[item[0]])
            entryBox.grid(
                column=1, row=self.TOP_ROW + idx + 1,
                columnspan=self.COL_WIDTH - 1, sticky="NSEW", padx=10, pady=5
            )

            # Make drug name field immutable if specified
            if self.drug_name_immutable is True:
                if item[0] == "drug_name":
                    entryBox["state"] = "disabled"

        # Create time between dose entry box
        anchor_row = self.TOP_ROW + len(items) + 1
        tk.Label(self.main_frame, text="Time Between Dose").grid(
            column=0, row=anchor_row,
            columnspan=1, sticky="NSEW", padx=5, pady=5
        )
        tk.Entry(self.main_frame, textvariable=self.prescription_data["time_btwn_dose"]).grid(
            column=1, row=anchor_row,
            columnspan=self.COL_WIDTH - 2, sticky="NSEW", padx=10, pady=5
        )
        # Special duration selector
        ttk.OptionMenu(self.main_frame, self.selected_duration_mod,
                       self.selected_duration_mod.get(), *self.duration_mods[0]).grid(
            column=self.COL_WIDTH - 1, row=anchor_row,
            columnspan=1, rowspan=1,
            padx=5, pady=5, sticky="NSEW"
        )

        # Date inputs
        for idx in range(len(date_items)):
            item = date_items[idx]
            anchor_row += 1

            # Set text box labels
            self.prescription_data[item[0]][0].set("MM")
            self.prescription_data[item[0]][1].set("DD")
            self.prescription_data[item[0]][2].set("YYYY")

            tk.Label(self.main_frame, text=item[1]).grid(
                column=0, row=anchor_row + idx,
                columnspan=1, sticky="NSEW", padx=5, pady=5
            )

            date_frame = tk.Frame(self.main_frame)
            date_frame.grid(
                column=1, row=anchor_row + idx,
                columnspan=3, sticky="NSEW",
                padx=5, pady=5
            )

            for jdx in range(len(self.prescription_data[item[0]])):
                tk.Entry(date_frame, textvariable=self.prescription_data[item[0]][jdx], width=6).grid(
                    column=jdx, row=0,
                    columnspan=1, sticky="NSEW", padx=5
                )

        # Create done and cancel buttons
        anchor_row += len(date_items)
        ttk.Button(self.main_frame, text="Cancel", command=self.root.destroy).grid(
            column=self.COL_WIDTH - 2, row=anchor_row,
            columnspan=1, sticky="SEW", padx=5, pady=8
        )
        self.done_button = ttk.Button(self.main_frame, text="Done", command=self.done_func)
        self.done_button.grid(
            column=self.COL_WIDTH - 1, row=anchor_row,
            columnspan=1, sticky="SEW", padx=5, pady=8
        )

    def get_time_btwn_dose_from_entry(self) -> int:
        """Convert time_between_dosage value into an integer number of seconds."""
        time_btwn_dose = int(int(self.prescription_data["time_btwn_dose"].get()) *
                         self.duration_mods[1][self.duration_mods[0].index(self.selected_duration_mod.get())])
        print(
            f'Result {time_btwn_dose} / Original {self.prescription_data["time_btwn_dose"].get()} / Mod {self.duration_mods[1][self.duration_mods[0].index(self.selected_duration_mod.get())]}')
        return time_btwn_dose

    def get_time_btwn_dose_info(self, time_btwn_dose: str) -> tuple:
        """Returns (1) the time between dosage adjusted for the determined duration mod and
        (2) the duration mod string."""
        try:
            seconds = int(time_btwn_dose)
        except ValueError:
            print("Bad int conversion with _MedicationInputParent.get_plausible_duration_mod in Medication.py. "
                  f'Using seconds as default.\nValue: "{self.prescription_data["time_btwn_dose"].get()}"')
            return -1, self.duration_mods[0][0]

        # Loop through duration_mods and check if a clean division can be done. If so, use that duration mod.
        for idx in reversed(range(len(self.duration_mods[0]))):
            if (seconds % int(self.duration_mods[1][idx])) == 0:
                return seconds // self.duration_mods[1][idx], self.duration_mods[0][idx]
        # Otherwise, just use seconds as a default if nothing sensible is found
        return seconds // self.duration_mods[1][0], self.duration_mods[0][0]


class AddMedicationWindow(_MedicationInputParent):
    def __init__(self, window_title, database, current_user):
        """Takes the shared elements and adds a prescription name input box."""
        super().__init__(window_title, self.click_done_button, database, current_user)

    def click_done_button(self, e=None):
        # Run validation tests
        validator = Validator()
        validator.check_dates_are_valid(self.prescription_data)
        validator.check_str_not_blank(self.prescription_data["drug_name"].get(), "Drug Name")
        validator.check_can_be_int(self.prescription_data["time_btwn_dose"].get(), "Time Between Dose")

        if validator.no_failures():
            # Automatically add "mg" to dosage
            dosage = self.prescription_data["dosage"].get()
            if f"{dosage[-2]}{dosage[-1]}" != "mg":
                dosage += "mg"

            # Add prescription to database
            self.database.add_prescription(
                self.current_user.get(),
                self.prescription_data["drug_name"].get(),
                self.prescription_data["doctor"].get(),
                self.get_time_btwn_dose_from_entry(),
                self.prescription_data["side_effects"].get(),
                dosage,
                int(self.prescription_data["date_issued"][2].get()),  # year
                int(self.prescription_data["date_issued"][0].get()),  # month
                int(self.prescription_data["date_issued"][1].get()),  # day
                int(self.prescription_data["expiration_date"][2].get()),  # year
                int(self.prescription_data["expiration_date"][0].get()),  # month
                int(self.prescription_data["expiration_date"][1].get()),  # day
            )

            self.root.destroy()

        else:
            validator.display_failures()


class EditMedicationWindow(_MedicationInputParent):
    def __init__(self, window_title, database, current_user):
        """Takes the shared elements and adds a prescription name input box."""
        super().__init__(window_title, self.click_done_button, database, current_user, drug_name_immutable=True)

        # Window size
        self.root.geometry('450x350')

        # OptionMenu selection variable
        self.selection = tk.StringVar()

        self.create_prescription_selection()
        self.update_prescription_selection()

        # Update prescription data fields when OptionMenu selection changes.
        self.selection.trace_add("write", self.update_prescription_selection)

        # Check that prescriptions exist to edit. If not, show an alert then close the window.
        validator = Validator()
        validator.check_user_has_prescriptions(self.current_user.get(), self.database)
        if not validator.no_failures():
            win = validator.display_failures()
            win.root.bind("<Destroy>", self.close_window)

    def create_prescription_selection(self):
        """Creates the selection box that allows the user to pick from their medications."""
        # Get an iterable list of the user's prescriptions and a copy with just the names.
        user_prescription_data = self.database.get_prescriptions_by_owner_ID(self.current_user.get())

        # Check if user has any prescriptions
        # If user has no prescriptions, show a blank box.
        if user_prescription_data is None:
            self.selection.set("")
            ttk.Label(self.main_frame, text="Current user has no prescriptions to edit!").grid(
                column=0, row=self.TOP_ROW - 1,
                columnspan=1, rowspan=1,
                padx=5, pady=10, sticky="NSEW"
            )
            self.done_button.state(['disabled'])  # Disable the done button if no prescriptions exist

        # If user has prescriptions, do as normal
        else:
            user_prescription_names = [x.drug_name for x in user_prescription_data]
            # Create label
            ttk.Label(self.main_frame, text="Select Prescription:").grid(
                column=0, row=self.TOP_ROW - 1,
                columnspan=1, rowspan=1,
                padx=5, pady=10, sticky="NSEW"
            )

            # Create selection widget
            combobox = ttk.OptionMenu(self.main_frame, self.selection,
                                      user_prescription_names[0], *user_prescription_names)
            combobox.grid(
                column=1, row=self.TOP_ROW - 1,
                columnspan=self.COL_WIDTH - 1, rowspan=1,
                padx=5, pady=10, sticky="NSEW"
            )

    def update_prescription_selection(self, *e):
        """Runs when a new prescription is selected from the option menu."""
        for prescription in self.database.prescriptions:
            if (prescription.owner_ID == self.current_user.get()) and (prescription.drug_name == self.selection.get()):
                self.prescription_data["drug_name"].set(prescription.drug_name)
                self.prescription_data["doctor"].set(prescription.doctor_name)
                self.prescription_data["side_effects"].set(prescription.side_effects)
                self.prescription_data["dosage"].set(prescription.dosage)
                self.prescription_data["date_issued"][2].set(prescription.date_issued.year)  # year
                self.prescription_data["date_issued"][0].set(prescription.date_issued.month)  # month
                self.prescription_data["date_issued"][1].set(prescription.date_issued.day)  # day
                self.prescription_data["expiration_date"][2].set(prescription.expiration_date.year)  # year
                self.prescription_data["expiration_date"][0].set(prescription.expiration_date.month)  # month
                self.prescription_data["expiration_date"][1].set(prescription.expiration_date.day)  # day

                # Set time between dose and duration mod combobox
                info = self.get_time_btwn_dose_info(prescription.time_btwn_dose)
                self.prescription_data["time_btwn_dose"].set(info[0])
                self.selected_duration_mod.set(info[1])
                break

    def click_done_button(self, e=None):
        # Run validation tests
        validator = Validator()
        validator.check_dates_are_valid(self.prescription_data)
        validator.check_str_not_blank(self.prescription_data["drug_name"].get(), "Drug Name")
        validator.check_can_be_int(self.prescription_data["time_btwn_dose"].get(), "Time Between Dose")

        if validator.no_failures():
            # Delete the old prescription
            self.database.delete_prescription_by_drug_name(
                self.selection.get(),
                self.current_user.get()
            )

            # Add the edited prescription
            self.database.add_prescription(
                self.current_user.get(),
                self.prescription_data["drug_name"].get(),
                self.prescription_data["doctor"].get(),
                self.get_time_btwn_dose_from_entry(),
                self.prescription_data["side_effects"].get(),
                self.prescription_data["dosage"].get(),
                int(self.prescription_data["date_issued"][2].get()),  # year
                int(self.prescription_data["date_issued"][0].get()),  # month
                int(self.prescription_data["date_issued"][1].get()),  # day
                int(self.prescription_data["expiration_date"][2].get()),  # year
                int(self.prescription_data["expiration_date"][0].get()),  # month
                int(self.prescription_data["expiration_date"][1].get()),  # day
            )

            self.root.destroy()

        else:
            validator.display_failures()

    def close_window(self, e=None):
        """Callback helper"""
        self.root.destroy()


class DeleteMedicationWindow:
    """Allows the user to select a medication to delete"""

    def __init__(self, database, current_user):
        # Open new window
        self.root = tk.Toplevel()

        # Database
        self.database = database
        self.current_user = current_user

        # Frames defined in other functions
        self.main_frame = None

        # Grid constants
        self.TOP_ROW = 1
        self.COL_WIDTH = 4

        # Colors
        self.DARK_GREY = "#b3b3b3"

        # Holds name of to-be-deleted prescription
        self.selection = tk.StringVar()

        # Run all the functions that create the window
        self.init_root()
        self.init_frames()
        self.create_title_bar()
        self.create_prescription_selection()
        self.create_buttons()

    def init_root(self):
        """Configure any window elements such as title, size, etc."""

        self.root.title('Delete Prescription: Medical Adherence Software - Group 7')  # Window title

        # Configure the root so that it does not interfere with the main_frame grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Window size
        self.root.geometry('450x200')
        self.root.resizable(width=True, height=True)

        # Window Logo
        logo = tk.PhotoImage(file='./assets/medical_icon.png')
        self.root.iconphoto(False, logo)

    def init_frames(self):
        """Configure the main and button frames."""
        # Main frame
        self.main_frame = tk.Frame(self.root, padx=3, pady=5)
        self.main_frame.grid(column=0, row=0, sticky="NSEW")

        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(self.TOP_ROW + 1, weight=1)

    def create_title_bar(self):
        """Creates a header"""
        tk.Label(self.main_frame, text="Delete Prescription", font=TITLE_FONT, background=self.DARK_GREY).grid(
            column=0, row=self.TOP_ROW - 1,
            columnspan=self.COL_WIDTH, rowspan=1,
            padx=5, pady=0, sticky="NEW"
        )

    def create_prescription_selection(self):
        """Creates the selection box that allows the user to pick from their medications."""
        # Get an iterable list of the user's prescriptions and a copy with just the names.
        user_prescription_data = self.database.get_prescriptions_by_owner_ID(self.current_user.get())

        # Check if user has any prescriptions
        # If user has no prescriptions, show a blank box.
        if user_prescription_data is None:
            self.selection.set("")
            ttk.Label(self.main_frame, text="Current user has no prescriptions to delete!").grid(
                column=0, row=self.TOP_ROW,
                columnspan=1, rowspan=1,
                padx=5, pady=10, sticky="NSEW"
            )

        # If user has prescriptions, do as normal
        else:
            user_prescription_names = [x.drug_name for x in user_prescription_data]
            # Create label
            ttk.Label(self.main_frame, text="Select Prescription:").grid(
                column=0, row=self.TOP_ROW,
                columnspan=1, rowspan=1,
                padx=5, pady=10, sticky="NSEW"
            )

            # Create selection widget
            combobox = ttk.OptionMenu(self.main_frame, self.selection,
                                      user_prescription_names[0], *user_prescription_names)
            combobox.grid(
                column=1, row=self.TOP_ROW,
                columnspan=self.COL_WIDTH - 1, rowspan=1,
                padx=5, pady=10, sticky="NSEW"
            )

    def create_buttons(self):
        """Creates done and cancel buttons."""
        ttk.Button(self.main_frame, text="Cancel", command=self.root.destroy).grid(
            column=self.COL_WIDTH - 2, row=self.TOP_ROW + 1,
            columnspan=1, sticky="SEW", padx=5, pady=8
        )
        delete_button = ttk.Button(self.main_frame, text="Delete", command=self.click_delete_button)
        delete_button.grid(
            column=self.COL_WIDTH - 1, row=self.TOP_ROW + 1,
            columnspan=1, sticky="SEW", padx=5, pady=8
        )

        # Disable delete button if no prescriptions exist for user
        if self.selection.get() == "":
            delete_button.state(['disabled'])

    def click_delete_button(self, e=None):
        """Delete selected prescription"""
        self.database.delete_prescription_by_drug_name(self.selection.get(), self.current_user.get())
        self.root.destroy()
