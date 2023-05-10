from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.DiscountType import DiscountType


class MaxComp(DiscountType):
    def __init__(self):
        super().__init__(0, "", "")

    def calculate(self, product, basket, total_price):
        pass
