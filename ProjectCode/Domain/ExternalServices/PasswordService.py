import re


class PasswordValidationService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Add any initialization code here
        return cls._instance

    # todo I think we should remove the statics

    @staticmethod
    def ValidatePassword(password):
        # Define regex patterns for each strength criteria
        length_pattern = r'^.{8,}$'  # Minimum length of 8 characters
        #uppercase_pattern = r'[A-Z]'  # At least one uppercase letter
        #lowercase_pattern = r'[a-z]'  # At least one lowercase letter

        # Check if password meets the criteria using regex
        if not re.match(length_pattern, password):
            return False
        #if not re.search(uppercase_pattern, password):
        #    return False
        #if not re.search(lowercase_pattern, password):
        #    return False

        # Password is considered strong if it passes all the criteria
        return True

    @staticmethod
    def ConfirmPassword(userPassword, givenPassword):  # todo we'll probably need to add hash
        return userPassword == givenPassword
