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
    from src.Medication import ViewMedicationWindow
except ImportError:
    from Prescription import Prescription
    from Medication import ViewMedicationWindow

ICO_PATH = path.abspath("./assets/medical_icon.png")
SNOOZE_TIME_MIN = 5

button_contents = (
    ("Medication Taken", "taken"),
    ("View Medication", "view"),
    ("Dismiss", "dismiss")
)


def check(database) -> list[Prescription]:
    """Takes a database and returns a tuple of prescriptions that need to have a notification sent out."""
    result = []

    for p in database.prescriptions:
        # Figure out if a prescription is due for a notification
        if datetime.now() >= p.was_taken + timedelta(seconds=int(p.time_btwn_dose)):
            # Then check if a snooze was applied and if that is done as well
            if p.snooze is None:
                result.append(p)
            elif datetime.now() - timedelta(minutes=SNOOZE_TIME_MIN) >= p.snooze:
                result.append(p)
                p.snooze = None

    return result


def send(database, presc: Prescription, current_user) -> None:
    """Takes input fields and sends a notification to remind the user to take medication"""
    # Checks that only the owner of the prescription receives the notification for their prescription
    if current_user.get() == presc.owner_ID:
        toaster = InteractableWindowsToaster("Medication Reminder")  # Sets title/initializes notification server

        # Configure notification body
        toast_body = Toast([f"Name: {presc.drug_name}\nDosage: {presc.dosage}\n" +
                            f"Expiration Date: {datetime.strftime(presc.expiration_date, '%B %d %Y')}"])  # Sets description text
        # toast_body.AddImage(ToastDisplayImage.fromPath(ICO_PATH))  # Display app logo
        toast_body.audio = ToastAudio(AudioSource.IM, looping=True)  # Gentle alarm sound until dismissed

        # Buttons
        for button in button_contents:
            toast_body.AddAction(ToastButton(button[0], button[1]))

        # Register callback functions
        toast_body.on_activated = lambda args: _button_handler(database, presc, current_user, args)
        toast_body.on_dismissed = lambda args: _snooze_action(database, presc)

        # Display notification
        toaster.show_toast(toast_body)


def _button_handler(database, presc, current_user, args) -> None:
    """Decides which button the user pressed and based on that, carries out the correct action."""
    arg = args.arguments

    if arg == "taken":
        _medication_taken_action(presc)
    elif arg == "view":
        _view_medication_action(presc, database, current_user)
    elif arg == "dismiss":
        _snooze_action(database, presc)
    else:
        _snooze_action(database, presc)  # Snooze if unknown action occurred


def _medication_taken_action(presc) -> None:
    """Sets the prescription in question as being taken just now."""
    presc.was_taken = datetime.now()


def _view_medication_action(presc, database, current_user) -> None:
    """Opens an editing window that displays the prescription's info"""
    # Temporarily disable the prescription's notification
    presc.snooze = datetime.now() + timedelta(weeks=1)  # If you take 1 week to look at your medication, you probably died so the notification running again is the least of your worries
    # Show medication information
    win = ViewMedicationWindow(f"View {presc.drug_name}", database, current_user, presc)
    win.root.bind("<Destroy>", lambda *args: _snooze_action(database, presc))  # Snoozes notification once user closes the window


def _snooze_action(database, presc: Prescription) -> None:
    """Runs when notification is dismissed by the dismiss button or otherwise.
    Essentially, this functions as a snooze. The user must take their medication soon, so it won't stop sending
    reminders until they do."""
    presc.snooze = datetime.now()
    #print(f"Snoozed {presc.drug_name} until {presc.snooze + timedelta(minutes=SNOOZE_TIME_MIN)}")
    database.save_prescriptions()
