from sqlite3 import Date


class SupplyService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Add any initialization code here
        return cls._instance

    def checkIfAvailable(self, store, user, products):
        return Date(2023, 12, 12)

    def call(self):
        return True
