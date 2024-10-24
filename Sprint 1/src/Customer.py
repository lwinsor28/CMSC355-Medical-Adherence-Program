"""
Name: Customer.py
Description: The customer class.
             Stores all the data belonging to an individual customer.
             This includes name, references to active prescriptions, etc.
"""

import uuid


class Customer:
    def __init__(self, first_name, last_name, username, password, email, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password  # Password stored in plaintext. This is terrible, but it doesn't matter here.
        self.email = email
        self.phone_number = phone_number
        self.ID = uuid.uuid4()  # Random ID to discern between customers with identical names, email, etc.
