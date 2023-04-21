class PasswordValidation:
    def __init__(self):
        pass
    #External service that will determinate if a password is strong enough

    @staticmethod
    def ValidatePassword(password):
        return True

    @staticmethod
    def ConfirmPassword(userPassword, givenPassword):
        return userPassword == givenPassword