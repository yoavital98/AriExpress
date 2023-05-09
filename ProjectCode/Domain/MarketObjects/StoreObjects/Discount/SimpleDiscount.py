from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.DiscountType import DiscountType


class SimpleDiscount(DiscountType):

    def __init__(self, percent, level, level_name):
        super().__init__(percent, level, level_name)

    def calculate(self, product, basket,total_price, category_or_product_id):
        if super()._checkIfRelevant(category_or_product_id):
            return self.percent
        else:
            return 0

