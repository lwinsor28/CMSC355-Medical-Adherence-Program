"""
Name: Notification.py
Description: Holds a wrapper function that sends the medication reminder notification.
"""

from windows_toasts import WindowsToaster, ToastDisplayImage, ToastAudio, AudioSource, Toast
from os import path

ICO_PATH = path.abspath("../assets/medical_icon.png")


def send(medication_name: str, description_text: str) -> None:
    """Takes input fields and sends a notification to remind the user to take medication"""
    toaster = WindowsToaster("Medication Reminder")  # Sets title/initializes notification server

    # Configure notification body
    toast_body = Toast()
    toast_body.text_fields = [f"{medication_name}\n{description_text}"]  # Sets description text
    toast_body.AddImage(ToastDisplayImage.fromPath(ICO_PATH))  # Display app logo
    toast_body.audio = ToastAudio(AudioSource.IM, looping=True)  # Gentle alarm sound until dismissed

    # Display notification
    toaster.show_toast(toast_body)


if __name__ == "__main__":
    send("Copium", "Default description text")
