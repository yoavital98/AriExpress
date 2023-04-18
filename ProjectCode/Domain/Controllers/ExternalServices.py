from ProjectCode.Domain.Objects.ExternalObjects.PasswordValidation import PasswordValidation
from ProjectCode.Domain.Objects.ExternalObjects.Paymet import Payment
from ProjectCode.Domain.Objects.ExternalObjects.Supply import Supply


class ExternalServices:
    def __init__(self):
        self.passwordValidator = PasswordValidation()
        self.paymentMethod = Payment()
        self.supplier = Supply()

    def fakeResponse(self):
        return "Geburtstag"
    