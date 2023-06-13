import requests


class SupplyService:
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
            raise Exception("Handshake request with SupplyService failed")

    def dispatch_supply(self, name, address, city, country, zipcode):
        post_data = {
            "action_type": "supply",
            "name": name,
            "address": address,
            "city": city,
            "country": country,
            "zip": zipcode
        }

        response = requests.post(self.paymentAddress, data=post_data)

        if response.status_code == 200:
            transaction_id = int(response.text)
            if transaction_id == -1:
                raise Exception("Supply transaction failed")
            else:
                return transaction_id
        else:
            raise Exception("Supply request failed")

    def cancel_supply(self, transaction_id):
        post_data = {
            "action_type": "cancel_supply",
            "transaction_id": str(transaction_id)
        }

        response = requests.post(self.paymentAddress, data=post_data)

        if response.status_code == 200:
            cancellation_result = int(response.text)
            if cancellation_result == -1:
                raise Exception("Supply cancellation failed")
            else:
                return True
        else:
            raise Exception("Supply cancellation request failed")