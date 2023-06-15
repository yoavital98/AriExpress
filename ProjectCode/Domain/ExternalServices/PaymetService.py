import requests


class PaymentService:
    _instance = None

    def __new__(cls, paymentAddress):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Add any initialization code here
            cls._instance.paymentAddress = str(paymentAddress)

        return cls._instance


    def perform_handshake(self):
        post_data = {
            "action_type": "handshake"
        }

        response = requests.post(self.paymentAddress, data=post_data)

        if response.status_code == 200:
            return True
        else:
            raise Exception("Handshake request with PaymentService failed")

    def pay(self, card_number, month, year, holder, ccv, id):
        post_data = {
            "action_type": "pay",
            "card_number": card_number,
            "month": month,
            "year": year,
            "holder": holder,
            "ccv": ccv,
            "id": id
        }


        response = requests.post(self.paymentAddress, data=post_data)

        if response.status_code == 200:
            transaction_id = int(response.text)
            if transaction_id == -1:
                raise Exception("Payment transaction failed")
            else:
                return transaction_id
        else:
            raise Exception("Payment request failed")


    def cancel_pay(self, transaction_id):
        post_data = {
            "action_type": "cancel_pay",
            "transaction_id": str(transaction_id)
        }

        response = requests.post(self.paymentAddress, data=post_data)

        if response.status_code == 200:
            cancellation_result = int(response.text)
            if cancellation_result == -1:
                raise Exception("Payment cancellation failed")
            else:
                return True
        else:
            raise Exception("Payment cancellation request failed")