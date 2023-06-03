import re
class PaymentService:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Add any initialization code here
        return cls._instance

    def validate_credit_card(self, card_number, expiration_date, cvv, cardholder_id):
        # Validate card number
        if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
            raise Exception("credit card number isn't valid")

        # Validate expiration date
        pattern = r"\d{2}/\d{2}"
        if not re.match(pattern, expiration_date):
            raise Exception("card date isn't valid")

        # Validate CVV
        if not cvv.isdigit() or len(cvv) != 3:
            raise Exception("CVV isn't valid")

        # Validate cardholder ID
        if not cardholder_id.isdigit() or len(cardholder_id) != 9:
            raise Exception("card holder ID isn't valid")

        # All checks passed, return True for a valid credit card
        return True

    def pay(self, store, card_number, card_user_name, card_user_ID, card_date, back_number, price): #TODO: Pass all the arguments
        if price > 20000:
            raise Exception("price too high, please contect your credit card company")
        return True

    def call(self):
        return True