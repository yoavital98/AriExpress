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
        return True

    @staticmethod
    def ConfirmPassword(userPassword, givenPassword):  # todo we'll probably need to add hash
        return userPassword == givenPassword
