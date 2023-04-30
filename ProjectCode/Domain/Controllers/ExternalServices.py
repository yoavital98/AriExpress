from ariExpressDjango.ProjectCode import PasswordValidation
from ariExpressDjango.ProjectCode import Payment
from ariExpressDjango.ProjectCode import Supply


class ExternalServices:
    def __init__(self):
        self.passwordValidator = PasswordValidation()
        self.paymentMethod = Payment()
        self.supplier = Supply()



    def ValidatePassword(self, password):
        return self.passwordValidator.ValidatePassword(password)


    def ConfirmePassword(self, password_1, password_2):
        return self.passwordValidator.ConfirmPassword(password_1, password_2)

    def pay(self, store, card_number, card_user_name, card_user_id, card_date, back_number, price):
        self.paymentMethod.pay(card_number, card_user_name, card_user_id, card_date, back_number, price)
