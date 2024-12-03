"""
Name: Notification.py
Description: Holds a wrapper function that sends the medication reminder notification.
"""

from windows_toasts import WindowsToaster, ToastDisplayImage, ToastAudio, AudioSource, Toast
from os import path

try:
    from src.Prescription import Prescription
except ImportError:
    from Prescription import Prescription

ICO_PATH = path.abspath("../assets/medical_icon.png")


def check(database) -> tuple[Prescription]:
    """Takes a database and returns a tuple of prescriptions that need to have a notification sent out."""
    pass


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
    db = Database()
    db.load_default_customers()
    db.load_default_prescriptions()

    send(db.prescriptions[0])
