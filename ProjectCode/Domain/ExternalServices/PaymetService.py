import requests


class PaymentService:
    _instance = None
    address_dict = {"default": "https://php-server-try.000webhostapp.com/"}
    request_address = "https://php-server-try.000webhostapp.com/"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def perform_handshake(self):
        post_data = {
            "action_type": "handshake"
        }

        response = requests.post(self.request_address, data=post_data)

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


        response = requests.post(self.request_address, data=post_data)

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

        response = requests.post(self.request_address, data=post_data)

        if response.status_code == 200:
            cancellation_result = int(response.text)
            if cancellation_result == -1:
                raise Exception("Payment cancellation failed")
            else:
                return True
        else:
            raise Exception("Payment cancellation request failed")

    def addUpdate_request_address(self, new_request_address, name):
        self.address_dict[name] = new_request_address
        self.request_address = new_request_address

    """ add name for specific or None for default"""
    def set_request_address(self, name=None):
        if not name:
            if name not in self.address_dict:
                raise Exception("Address not found")
            self.request_address = self.address_dict[name]
        self.request_address = "https://php-server-try.000webhostapp.com/"

    def get_request_address(self, name):
        if name not in self.address_dict:
            raise Exception("Address not found")
        return self.address_dict[name]
