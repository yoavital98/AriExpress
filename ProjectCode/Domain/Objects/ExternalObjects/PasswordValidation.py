class PasswordValidation:
    def __init__(self):
        pass
    #External service that will determinate if a password is strong enough
    def ValidatePassword(self, password):
        return True
    def ConfirmePassword(self,userPassword,givenPassword):
        return userPassword == givenPassword