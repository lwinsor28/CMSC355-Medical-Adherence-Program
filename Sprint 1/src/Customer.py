"""
Name: Customer.py
Description: The customer class.
             Stores all the data belonging to an individual customer.
             This includes name, references to active prescriptions, etc.
"""

import uuid
from datetime import datetime


class Customer:
    def __init__(self, first_name: str, last_name: str,
                 username: str, password: str, email: str,
                 phone_number: str, date_of_birth: datetime):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password  # Password stored in plaintext. This is terrible, but it doesn't matter here.
        self.email = email
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth  # FIXME: This isn't in the data description, but is shown in the prototype image
        self.ID = uuid.uuid4()  # Random ID to discern between customers with identical names, email, etc.

    def __str__(self):
        return "{0} {1}, {2}, {3}, {4}, {5}, {6}, {7}".format(
            self.first_name, self.last_name, self.username,
            self.password, self.email, self.phone_number,
            str(self.date_of_birth), self.ID
        )
