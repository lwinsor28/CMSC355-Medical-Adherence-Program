"""
Name: Prescription.py
Description: The prescription class.
             Stores all the data belonging to an individual prescription
             This includes drug name, issuing doctor's name, etc. as specified in
             the requirement specification document.
"""

import uuid
from datetime import datetime


class Prescription:
    def __init__(self, owner_ID: str,
                 drug_name: str, doctor_name: str,
                 time_btwn_dose: int, side_effects: str, dosage: str,
                 date_issued_year: int, date_issued_month: int, date_issued_day: int,
                 expiration_date_year: int, expiration_date_month: int, expiration_date_day: int):
        self.owner_ID = owner_ID  # ID of the Customer object that was logged in upon creation.
        self.drug_name = drug_name
        self.doctor_name = doctor_name
        self.time_btwn_dose = time_btwn_dose  # Seconds
        self.side_effects = side_effects
        self.dosage = dosage

        # Random ID to discern between prescriptions with identical names, date, etc.
        self.ID = uuid.uuid4()

        # Dates are special.
        self.date_issued = datetime(date_issued_year, date_issued_month, date_issued_day)
        self.expiration_date = datetime(expiration_date_year, expiration_date_month, expiration_date_day)

    def __str__(self):
        return """Name: {0}
        Doctor: {1}
        Dosage: {2}
        Time Between Doses: {3}
        Side Effects: {4}
        Date Issued: {5}
        Date Expiration: {6}
        ID: {7}""".format(
            self.drug_name, self.doctor_name,
            self.dosage,
            self.time_btwn_dose,
            self.side_effects,
            self.date_issued.isoformat(), self.expiration_date.isoformat(),
            self.ID
        )
