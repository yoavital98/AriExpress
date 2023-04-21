class PasswordValidation:
    def __init__(self):
        pass
    #External service that will determinate if a password is strong enough
    def ValidatePassword(self, password):
        # todo add terms for legal password - let's assume password needs to have at least 8 chars,
        # todo one of them is capital letter and small letter
        return True
    def ConfirmePassword(self,userPassword,givenPassword):
        return userPassword == givenPassword