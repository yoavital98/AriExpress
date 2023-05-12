from ProjectCode.Domain.MarketObjects.StoreObjects.Policy import Policy


class MaxComp(Policy):
    def __init__(self):
        super().__init__(0, "", "")

    def calculate(self, product, basket, total_price):
        pass
