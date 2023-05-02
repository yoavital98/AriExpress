class PaymentService:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Add any initialization code here
        return cls._instance

    def process_payment(self, card_number, card_user_name, card_user_id, card_date, back_number, price):
        # Your payment processing logic goes here
        return True
    def pay(self, store, card_number, card_user_name, card_user_ID, card_date, back_number, price): #TODO: Pass all the arguments
        return True