"""
Name: Database.py
Description: The database class.
             Serves as a home for all the data stored in this application.
             It holds a list of all customers and a list of all active prescriptions.
"""

import pickle

try:
    from src.Customer import Customer
except ImportError:
    from Customer import Customer


class Database:
    def __init__(self):
        self.customers = []
        self.prescriptions = []

        self.CUSTOMER_FILE_NAME = "customers.pkl"
        self.PRESCRIPTION_FILE_NAME = "prescriptions.pkl"

    # CUSTOMER MANAGEMENT METHODS -----
    def add_customer(self, first_name, last_name, username, password, email, phone_number, date_of_birth) -> str:
        """Adds new customer to database. Returns ID of new user"""
        new_customer = Customer(first_name, last_name, username, password, email, phone_number, date_of_birth)
        self.customers.append(new_customer)
        return new_customer.ID

    def get_customer_by_ID(self, ID):
        """Get customer object by ID. Returns None if no customer with ID exists."""
        for customer in self.customers:
            if customer.ID == ID:
                return customer

        return None

    def get_customer_by_username_password(self, username, password):
        """Get customer object by matching username and password. Returns None if no matching customer exists."""
        for customer in self.customers:
            if (customer.username == username) and (customer.password == password):
                return customer

        return None

    # PRESCRIPTION MANAGEMENT METHODS -----
    def add_prescription(self):
        """Adds new prescription to database"""
        # FIXME: Not implemented in sprint 1
        pass

    def save_customers(self):
        """Save customers list to disk"""
        with open(self.CUSTOMER_FILE_NAME, "wb") as file:
            pickle.dump(self.customers, file)

    def save_prescriptions(self):
        """Save prescriptions"""
        # FIXME: Implement in later sprint. Likely just a trivial copy/paste of save_customers()
        pass

    def save_all(self):
        """Save whole database to disk"""
        self.save_customers()
        self.save_prescriptions()

    def load(self):
        """Loads saved data from disk"""
        with open(self.CUSTOMER_FILE_NAME, "rb") as file:
            self.customers = pickle.load(file)
        # FIXME: Add prescription loading
        # FIXME: No error handling to check if files exist

    def __str__(self):
        result = "Customers (" + str(len(self.customers)) + ") " + "-" * 10 + "\n"
        for customer in self.customers:
            result += " - " + str(customer) + "\n"
        # FIXME: Implement prescriptions here if desired
        return result


if __name__ == "__main__":
    # Quick sanity test
    # The following is only execute if this exact file is run by itself
    import datetime

    db = Database()
    dob1 = datetime.date.fromisoformat("1989-12-07")
    dob2 = datetime.date.fromisoformat("2018-06-01")
    db.add_customer("Satoru", "Gojo", "thestr0ngest", "hollow&purple1989",
                    "satorugojo@jjhs.edu", "5551234567", dob1)
    db.add_customer("Sukuna", "Ryoumen", "kingofcurses", "20fingers",
                    "imhim@malevolentshrine.lol", "5556666666", dob2)
    db.save_all()

    db2 = Database()
    db2.load()

    if str(db) == str(db2):
        print("Save/load test successful")
    else:
        print("Save/load test unsuccessful")
