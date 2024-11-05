"""
Name: Database.py
Description: The database class.
             Serves as a home for all the data stored in this application.
             It holds a list of all customers and a list of all active prescriptions.
"""

import pickle

try:
    from src.Customer import Customer
    from src.Prescription import Prescription
except ImportError:
    from Customer import Customer
    from Prescription import Prescription


class Database:
    def __init__(self):
        self.customers = []
        self.prescriptions = []

        self.CUSTOMER_FILE_NAME = "customers.pkl"
        self.PRESCRIPTION_FILE_NAME = "prescriptions.pkl"

    # CUSTOMER MANAGEMENT METHODS -----
    def add_customer(self, first_name, last_name, username, password, email, phone_number) -> Customer:
        """Adds new customer to database. Returns object of the new user"""
        new_customer = Customer(first_name, last_name, username, password, email, phone_number)
        self.customers.append(new_customer)
        return new_customer.ID

    def get_customer_by_ID(self, ID: str) -> Customer or None:
        """Get customer object by ID. Returns None if no customer with ID exists."""
        for customer in self.customers:
            if str(customer.ID) == str(ID):
                return customer

        return None

    def get_customer_by_username_password(self, username, password) -> Customer or None:
        """Get customer object by matching username and password. Returns None if no matching customer exists."""
        for customer in self.customers:
            if (customer.username == username) and (customer.password == password):
                return customer

        return None

    # PRESCRIPTION MANAGEMENT METHODS -----
    def add_prescription(self, owner_ID: str, drug_name: str, doctor_name: str, time_btwn_dose: int, side_effects: str,
                         date_issued_year: int, date_issued_month: int, date_issued_day: int,
                         expiration_date_year: int, expiration_date_month: int, expiration_date_day: int) -> str:
        """Adds new prescription to database.
        Returns the ID of the new prescription."""
        new_prescription = Prescription(
            owner_ID, drug_name, doctor_name, time_btwn_dose, side_effects,
            date_issued_year, date_issued_month, date_issued_day,
            expiration_date_year, expiration_date_month, expiration_date_day
        )
        self.prescriptions.append(new_prescription)
        return new_prescription.ID

    def get_prescription_by_ID(self, ID: str) -> Prescription or None:
        """Finds prescription in database from a given unique ID. Returns None if no match exists."""
        for prescription in self.prescriptions:
            if prescription.ID == ID:
                return prescription

        return None

    def get_prescription_by_owner_ID(self, user_id: str) -> tuple[Prescription] or None:
        """Find all prescriptions owned by the given user. Returns None if no match is found"""
        result = []
        for prescription in self.prescriptions:
            if prescription.owner_ID == user_id:
                result.append(prescription)

        return tuple(result) if len(result) != 0 else None

    # SAVING METHODS -----
    def save_customers(self) -> None:
        """Save customers list to disk"""
        with open(self.CUSTOMER_FILE_NAME, "wb") as file:
            pickle.dump(self.customers, file)

    def save_prescriptions(self) -> None:
        """Save prescriptions list to disk"""
        with open(self.PRESCRIPTION_FILE_NAME, "wb") as file:
            pickle.dump(self.prescriptions, file)

    def save_all(self) -> None:
        """Save whole database to disk"""
        self.save_customers()
        self.save_prescriptions()

    def load(self) -> None:
        """Loads saved data from disk"""
        # Customers
        try:
            with open(self.CUSTOMER_FILE_NAME, "rb") as file:
                self.customers = pickle.load(file)
        except (OSError, ModuleNotFoundError):
            print("No customer file could be loaded. Loading in defaults...")
            self.load_default_customers()
            self.save_customers()

        # Prescriptions
        try:
            with open(self.PRESCRIPTION_FILE_NAME, "rb") as file:
                self.prescriptions = pickle.load(file)
        except (OSError, ModuleNotFoundError):
            print("No database file could be loaded. Loading in defaults...")
            self.load_default_prescriptions()
            self.save_prescriptions()

    def load_default_customers(self) -> None:
        """Loads 2 default customers into database. Assumes empty database, so does not check for username conflicts."""
        self.add_customer("Satoru", "Gojo", "thestr0ngest", "hollow&purple1989",
                          "satorugojo@jjhs.edu", "5551234567")
        self.add_customer("Sukuna", "Ryoumen", "kingofcurses", "20fingers",
                          "imhim@malevolentshrine.lol", "5556666666")

    def load_default_prescriptions(self) -> None:
        """Loads 2 default prescriptions for default user `Satoru`.
        Note, this leaves the 2nd default user `Sukuna` without prescriptions on purpose for testing."""
        gojo = self.get_customer_by_username_password("thestr0ngest", "hollow&purple1989")
        self.add_prescription(gojo.ID, "Copium", "Gege Akutami", 60*60*24*7, "Sudden torso separation.",
                              2023, 9, 25, 2024, 9, 29)
        self.add_prescription(gojo.ID, "Reverse Cursed Technique", "Ieiri Shoko", 60*2,
                              "Temporary loss of mental faculties.",
                              2019, 9, 9, 2024, 9, 29)

    def __str__(self):
        result = "Customers (" + str(len(self.customers)) + ") " + "-" * 10 + "\n"
        for customer in self.customers:
            result += " - " + str(customer) + "\n"
        result += "Prescriptions (" + str(len(self.prescriptions)) + ") " + "-" * 10 + "\n"
        for prescription in self.prescriptions:
            result += " - " + str(prescription) + "\n"
        return result


if __name__ == "__main__":
    # Quick sanity test
    # The following is only execute if this exact file is run by itself
    db = Database()
    db.load_default_customers()
    db.load_default_prescriptions()

    db.CUSTOMER_FILE_NAME = "temp_cust.pkl"
    db.PRESCRIPTION_FILE_NAME = "temp_pscr.pkl"
    db.save_all()

    db2 = Database()
    db2.CUSTOMER_FILE_NAME = db.CUSTOMER_FILE_NAME
    db2.PRESCRIPTION_FILE_NAME = db.PRESCRIPTION_FILE_NAME
    db2.load()

    print(str(db))

    if str(db) == str(db2):
        print("Save/load test successful")
    else:
        print("Save/load test unsuccessful")

    import os
    if os.path.exists(db.CUSTOMER_FILE_NAME):
        os.remove(db.CUSTOMER_FILE_NAME)
    if os.path.exists(db.PRESCRIPTION_FILE_NAME):
        os.remove(db.PRESCRIPTION_FILE_NAME)
