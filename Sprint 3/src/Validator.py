"""
Name: Validator.py
Description: Implements a simple class interface to keep track of user input issues.

The way this class should be used is the following:
    1. Instantiate a new instance of the Validator class inside any operation you wish to validate input.
    2. Run appropriate "check" functions.
    3. Run no_failures() to see if any validation checks failed.
        If failures exist, the function returns False. It will also pull up a popup showing error messages to the
        user so that they can fix their input.
        If failures do not exist, the function returns True.
    4. Do not continue regular execution until the no_failures can be satisfied.
        The class does not "reset" itself. It assumes you will create a new instance for the next try, however
        that will be implemented.

Feel free to add a new validation function into the class if necessary.
"""

import re
from datetime import datetime

try:
    from src.Database import Database
    from src.Alert import AlertWindow
except ImportError:
    from src.Database import Database
    from src.Alert import AlertWindow


class Validator:
    def __init__(self):
        self._failed_cases = []  # Contains error messages from failed validation cases

    def no_failures(self) -> bool:
        """Looks at self._failed_cases and sees if any fail cases exist.

        Returns True if no failed cases exist and execution should resume as normal.
        Returns False is failed cases exist and an alternate execution path should be taken to allow the
        user to fix the issues with their input."""

        # All is good, return true
        if len(self._failed_cases) == 0:
            return True

        # All is not good
        else:
            return False

    def display_failures(self) -> AlertWindow:
        """
        Display an alert window containing all validation failure messages.
        """
        alert_message = ""
        for message in self._failed_cases:
            alert_message += message + "\n"
        return AlertWindow(alert_message)

    def _add_failure(self, fail_message: str) -> None:
        """Adds failure message to self._failed_cases"""
        self._failed_cases.append(fail_message)

    def __str__(self):
        if len(self._failed_cases) == 0:
            return "No failed cases."
        else:
            result = "Failed cases:"
            for message in self._failed_cases:
                result += f"\n\t{message}"
            return result

    """
    VALIDATOR CHECK FUNCTIONS BELOW ------------------------------------------------------------------------------------
    The following are various test cases that are called throughout the program.
    None of them are *expected* to be used outside their original, intended context, but reuse is permitted
    and should not break anything.
    """

    def check_username_does_not_exist(self, username: str, database: Database) -> None:
        """
        Checks the given database if the given username is already in use.
        Test case implementation: Use Case 2, TC02
        """
        FAIL_MESSAGE = "Username already exists in the database. Please choose another username."

        for user in database.customers:
            if user.username == username:
                self._add_failure(FAIL_MESSAGE)

    def check_valid_email_format(self, email: str) -> None:
        """
        Checks if email is in a valid format.
        Test case implementation: Use Case 2, TC03
        """
        FAIL_MESSAGE = "Email was not in the correct format. Please enter a valid email address."

        EMAIL_REGEX = r"[a-zA-Z0-9!#\$%&'\*\+-/=\?\^_`\{\|\}~\.]+@[a-zA-Z0-9\-]+\.[a-zA-Z\.]+"  # Yes, I know.
        """
        The above isn't a perfect representation of the standard, but covers enough. It's mostly lacking
        support for "comments" and checking if certain characters are present only within quotes.
        I've never seen an email that uses either of these features, and just putting your email in won't fail
        in the way it's been implemented. If you like to use comments in your email address, too bad!
        """

        if re.fullmatch(EMAIL_REGEX, email) is None:  # re.fullmatch() returns None if the entire string does not match
            self._add_failure(FAIL_MESSAGE)

    def check_valid_password_format(self, password: str) -> None:
        """
        Checks is password satisfied the following requirements:
        * Has 8 or more characters
        * Contains both letters and numbers
        Test case implementation: Use Case 2, TC04
        """
        FAIL_MESSAGE_CHARS = "Password does not satisfy the requirements; it must have eight or more characters."
        FAIL_MESSAGE_LETTERS_AND_NUMS = "Password does not satisfy the requirements; " + \
                                        "it must have both letters and numbers."

        EIGHT_CHARS_REGEX = ".{8,}"
        LETTERS_THEN_NUM_REGEX = ".*[0-9].*[a-zA-Z].*"
        NUM_THEN_LETTERS_REGEX = ".*[a-zA-Z].*[0-9].*"

        # Check for length requirement
        if re.fullmatch(EIGHT_CHARS_REGEX, password) is None:  # re.fullmatch() returns None if no match
            self._add_failure(FAIL_MESSAGE_CHARS)

        # Check for letters and numbers requirement
        if (re.fullmatch(LETTERS_THEN_NUM_REGEX, password) is None) and \
                (re.fullmatch(NUM_THEN_LETTERS_REGEX, password) is None):
            self._add_failure(FAIL_MESSAGE_LETTERS_AND_NUMS)

    def check_username_exists(self, username: str, database: Database) -> None:
        """
        Checks the given database if the given username has an account associated with it.
        Test case implementation: Use Case 2, TC06
        """
        FAIL_MESSAGE = f"No account found with username {username}."

        for user in database.customers:
            if user.username == username:
                return
        self._add_failure(FAIL_MESSAGE)

    def check_username_password_match(self, username: str, password: str, database: Database) -> None:
        """
        Checks the given database if the given username and password correctly match an existing user.
        Test case implementation: Use Case 2, TC07
        """
        FAIL_MESSAGE = f"Password for user \"{username}\" incorrect. Please try again."

        for user in database.customers:
            if user.username == username:
                if user.password == password:
                    return
                else:
                    break
        self._add_failure(FAIL_MESSAGE)

    def check_user_logged_in(self, current_user_ID, no_user_msg) -> None:
        """
        Makes sure user is logged in before the prescriptions menu can be accessed.
        Test case implementation: Use Case 1, TC06
        """
        FAIL_MESSAGE = "No user logged in. Please login to an account before accessing this menu!"

        if current_user_ID == no_user_msg:
            self._add_failure(FAIL_MESSAGE)

    # Validation cases not used in any specific test cases, but included to preserve functionality of the app.

    def check_dates_are_valid(self, prescription_data: dict) -> None:
        """Make sure that prescription date fields are valid integers."""
        FAIL_MESSAGE = "The date(s) are invalid in some regard. Please input valid dates."

        try:
            datetime(int(prescription_data["date_issued"][2].get()),
                     int(prescription_data["date_issued"][0].get()),
                     int(prescription_data["date_issued"][1].get())
                     )
            datetime(int(prescription_data["expiration_date"][2].get()),
                     int(prescription_data["expiration_date"][0].get()),
                     int(prescription_data["expiration_date"][1].get())
                     )

        except ValueError:
            self._add_failure(FAIL_MESSAGE)

    def check_str_not_blank(self, input_str: str, field_name: str) -> None:
        """Check that the given string is not blank. Useful to make sure usernames/prescription names are not blank."""
        FAIL_MESSAGE = f"{field_name.title()} cannot be blank."

        if (input_str is None) or (input_str == ""):
            self._add_failure(FAIL_MESSAGE)

    def check_can_be_int(self, input_str: str, field_name: str) -> None:
        """Checks a string to make sure it can be converted to an integer."""
        FAIL_MESSAGE = f"{field_name} must be a number." \
                       f"Please remove any non-numeric characters from \"{input_str}\"."

        if not input_str.isdigit():
            self._add_failure(FAIL_MESSAGE)

    def check_user_has_prescriptions(self, user_id: str, database: Database) -> None:
        """Check that given user has any prescriptions."""
        FAIL_MESSAGE = "Current user has no prescriptions to edit!"

        for prescription in database.prescriptions:
            if prescription.owner_ID == user_id:
                return

        self._add_failure(FAIL_MESSAGE)


"""Some manual testing of test cases is performed here if this file is run by itself."""
if __name__ == "__main__":
    # Fake database
    db = Database()
    db.add_customer("Satoru", "Gojo", "thestr0ngest", "hollow&purple1989",
                    "satorugojo@jjhs.edu", "5551234567")

    # check_username_does_not_exist
    v = Validator()
    v.check_username_does_not_exist("joemamma", db)
    print(f"Blank / {str(v)}")
    v.check_username_does_not_exist("", db)
    print(f"Blank / {str(v)}")
    v.check_username_does_not_exist("thestr0ngest", db)
    print(f"Username exists / {str(v)}")

    # check_valid_emai_format
    v = Validator()
    v.check_valid_email_format("joe@mama.com")
    v.check_valid_email_format("MrEmail@gmail.com")
    print(f"Blank / {str(v)}")
    v.check_valid_email_format(r"we}rde3mai|e@epic.co.uk")
    print(f"Blank / {str(v)}")
    v.check_valid_email_format("noat.com")
    v.check_valid_email_format("@invalid.ninja")
    v.check_valid_email_format("よくない@invalid.jp")
    v.check_valid_email_format("bad@domain")
    print(f"4 Email Failures / {str(v)}")

    # check_valid_password_format
    v = Validator()
    v.check_valid_password_format("password1")
    v.check_valid_password_format("365proTECTion")
    v.check_valid_password_format("@epicHAX40R!")
    print(f"Blank / {str(v)}")
    v.check_valid_password_format("toofew1")
    print(f"Password Failure, too few / {str(v)}")
    v = Validator()
    v.check_valid_password_format("NOnumbers")
    v.check_valid_password_format("1337420999")
    print(f"2 Password Failures, needs letters & nums / {str(v)}")
    v = Validator()
    v.check_valid_password_format("allbad")
    print(f"Password Failure, both in one / {str(v)}")

    # check_username_exists
    v = Validator()
    v.check_username_exists("thestr0ngest", db)
    print(f"Blank / {str(v)}")
    v.check_username_exists("i-dont-exist", db)
    print(f"Username does not exist / {str(v)}")

    # check_username_password_match
    v = Validator()
    v.check_username_password_match("thestr0ngest", "hollow&purple1989", db)
    print(f"Blank / {str(v)}")
    v.check_username_password_match("thestr0ngest", "fakepassword", db)
    print(f"Password failure / {str(v)}")
    v = Validator()
    v.check_username_exists("i-dont-exist", db)
    v.check_username_password_match("i-dont-exist", "fakepassword", db)
    print(f"Username & Password failure / {str(v)}")
