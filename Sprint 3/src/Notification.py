"""
Name: Notification.py
Description: Holds a wrapper function that sends the medication reminder notification.
"""

from windows_toasts import WindowsToaster, ToastDisplayImage, ToastAudio, AudioSource, Toast
from os import path
from datetime import datetime

try:
    from src.Prescription import Prescription
except ImportError:
    from Prescription import Prescription

ICO_PATH = path.abspath("./assets/medical_icon.png")


def check(database) -> list[Prescription]:
    """Takes a database and returns a tuple of prescriptions that need to have a notification sent out."""
    result = []
    for p in database.prescriptions:
        delta = datetime.now() - p.was_taken
        delta = delta.seconds
        if delta >= int(p.time_btwn_dose):
            result.append(p)

    return result


def send(prescription: Prescription) -> None:
    """Takes input fields and sends a notification to remind the user to take medication"""
    toaster = WindowsToaster("Medication Reminder")  # Sets title/initializes notification server

    # Configure notification body
    toast_body = Toast()
    toast_body.text_fields = [f"{prescription.drug_name}\nNeed to take now!"]  # Sets description text
    toast_body.AddImage(ToastDisplayImage.fromPath(ICO_PATH))  # Display app logo
    toast_body.audio = ToastAudio(AudioSource.IM, looping=True)  # Gentle alarm sound until dismissed

    # Display notification
    toaster.show_toast(toast_body)


if __name__ == "__main__":
    try:
        from src.Database import Database
    except ImportError:
        from Database import Database

    ICO_PATH = path.abspath("../assets/medical_icon.png")
    db = Database()
    db.load_default_customers()
    db.load_default_prescriptions()

    #send(db.prescriptions[0])

    print("Queue:")
    queue = check(db)
    for prescription in queue:
        print(f"\t{prescription.drug_name} / {prescription.ID}")
