"""
Name: Customer.py
Description: The customer class.
             Stores all the data belonging to an individual customer.
             This includes name, references to active prescriptions, etc.
"""

import uuid


class Customer:
    def __init__(self, first_name: str, last_name: str,
                 username: str, password: str, email: str,
                 phone_number: str):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password  # Password stored in plaintext. This is terrible, but it doesn't matter here.
        self.email = email
        self.phone_number = phone_number
        self.ID = str(uuid.uuid4())  # Random ID to discern between customers with identical names, email, etc.

    def __str__(self):
        return "Name: {0} {1},\nUsername/Password: {2}, {3},\nEmail/Phone: {4}, {5},\nID: {6}".format(
            self.first_name, self.last_name,
            self.username, self.password,
            self.email, self.phone_number,
            self.ID
        )
