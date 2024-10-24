"""
Name: Database.py
Description: The database class.
             Serves as a home for all the data stored in this application.
             It holds a list of all customers and a list of all active prescriptions.
"""

import Customer


class Database:
    def __init__(self):
        self.customers = []
        self.prescriptions = []

    # CUSTOMER MANAGEMENT METHODS -----
    def add_customer(self, first_name, last_name, username, password, email, phone_number):
        # Adds new customer to database
        new_customer = Customer(first_name, last_name, username, password, email, phone_number)
        self.customers.append(new_customer)

    def get_customer_by_ID(self, ID):
        # Get customer object by ID. Returns None if no customer with ID exists.
        for customer in self.customers:
            if customer.ID == ID:
                return customer

        return None

    # PRESCRIPTION MANAGEMENT METHODS -----
    def add_prescription(self):
        # Adds new prescription to database
        # FIXME: Not implemented in sprint 1
        pass

    def save(self):
        # Save database to disk
        # FIXME: Do we want to implement this or just have it be all in RAM? - Trevor 2024/10/24
        pass
