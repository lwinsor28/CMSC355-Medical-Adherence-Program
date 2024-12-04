"""
Name: Notification.py
Description: Holds a wrapper function that sends the medication reminder notification.
"""

from windows_toasts import InteractableWindowsToaster, ToastDisplayImage, ToastAudio, AudioSource, Toast, \
    ToastActivatedEventArgs, ToastButton
from os import path
from datetime import datetime, timedelta

try:
    from src.Prescription import Prescription
except ImportError:
    from Prescription import Prescription

ICO_PATH = path.abspath("./assets/medical_icon.png")
SNOOZE_TIME_SEC = 300  # 5 minutes

button_contents = (
    ("Medication Taken", "taken"),
    ("View Medication", "view"),
    ("Dismiss", "dismiss")
)


def check(database) -> list[Prescription]:
    """Takes a database and returns a tuple of prescriptions that need to have a notification sent out."""
    result = []
    for p in database.prescriptions:
        delta = datetime.now() - p.was_taken
        delta = delta.seconds
        print(f"{p.drug_name} delta: {delta} >= {int(p.time_btwn_dose) + p.snooze} / {delta >= (int(p.time_btwn_dose) + p.snooze)}")
        if delta >= (int(p.time_btwn_dose) + p.snooze):
            result.append(p)

    return result


def send(database, presc: Prescription, current_user) -> None:
    """Takes input fields and sends a notification to remind the user to take medication"""
    toaster = InteractableWindowsToaster("Medication Reminder")  # Sets title/initializes notification server

    # Configure notification body
    toast_body = Toast([f"{presc.drug_name}\nNeed to take now!"])  # Sets description text
    # toast_body.AddImage(ToastDisplayImage.fromPath(ICO_PATH))  # Display app logo
    toast_body.audio = ToastAudio(AudioSource.IM, looping=True)  # Gentle alarm sound until dismissed

    # Buttons
    for button in button_contents:
        toast_body.AddAction(ToastButton(button[0], button[1]))

    toast_body.on_activated = lambda args: _button_handler(database, presc, current_user, args)
    toast_body.on_dismissed = lambda args: _snooze_action(database, presc)

    # Display notification
    toaster.show_toast(toast_body)


def _button_handler(database, presc, current_user, args) -> None:
    """Decides which button the user pressed and based on that, carries out the correct action."""
    arg = args.arguments

    if arg == "dismiss":
        _snooze_action(database, presc)
    else:
        print(f"Not dismissed / {args.arguments}")
        _snooze_action(database, presc)  # Snooze if unknown action occurred


def _snooze_action(database, presc: Prescription) -> None:
    """Runs when notification is dismissed by the dismiss button or otherwise.
    Essentially, this functions as a snooze. The user must take their medication soon, so it won't stop sending
    reminders until they do."""
    presc.snooze += SNOOZE_TIME_SEC
    print(f"Snoozed {presc.drug_name} until {presc.was_taken + timedelta(seconds=int(presc.time_btwn_dose))}")
    database.save_prescriptions()


if __name__ == "__main__":
    try:
        from src.Database import Database
    except ImportError:
        from Database import Database

    ICO_PATH = path.abspath("../assets/medical_icon.png")
    db = Database()
    db.load_default_customers()
    db.load_default_prescriptions()

    # send(db, db.prescriptions[0])

    print("Queue:")
    queue = check(db)
    for prescription in queue:
        print(f"\t{prescription.drug_name} / {prescription.ID}")
