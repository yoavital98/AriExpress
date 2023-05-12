from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.DiscountType import DiscountType


class SecretDiscount(DiscountType):
    def __init__(self):
        pass

    def calculate(self, product, basket, total_price, category_or_product_id):
        pass
