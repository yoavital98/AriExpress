class ExternalServices:
    def __init__(self):
        self.passwordValidator = PasswordValidation()
        self.paymentMethod = Payment()
        self.supplier = Supply()

    def fakeResponse(self):
        return "Geburtstag"
    