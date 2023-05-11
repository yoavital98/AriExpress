from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.AddComp import AddComp
from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.ConditionedDiscount import ConditionedDiscount
from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.DiscountType import DiscountType
from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.SimpleDiscount import SimpleDiscount


class DiscountPolicy:

    # IMPORTANT!!: only root discount have an ID
    # for example: child of Add discount wont have an ID
    def __init__(self):
        self.discounts = TypedDict(int, DiscountType)
        self.discount_id = 0

    """
        kwargs := 
            discount_type := Conditioned | Simple | Coupon | Max | Add
            percent := 0-100 int value
            level := "Store" | "Category" | "Product"
            level_name := product_id | category name | "" blank for store
            rule := RuleComp (optional)
            discounts := Dict(str, DiscountType)
            Example: {"1": {"discount_type": "Simple" ....}, "2": {"discount_type": "Coupon"...} }
    """
    def addDiscount(self, **kwargs):
        discount = None
        discount_type, percent, level = kwargs["discount_type"], kwargs["percent"], kwargs["level"]
        level_name, rule = kwargs["level_name"], kwargs["rule"]
        if discount_type == "Conditioned":
            if not rule:
                raise Exception("Conditioned discount must contain a rule")
            discount = ConditionedDiscount(percent, level, level_name, rule)
        elif discount_type == "Add":
            discount = AddComp(kwargs["discounts"])
        elif discount_type == "Max": #TODO: impl max discount
            pass
        elif discount_type == "Simple":
            discount = SimpleDiscount(percent, level, level_name)
        elif discount_type == "Coupon": #TODO: impl coupon discount
            pass
        else:
            raise Exception("No such discount type exists")
        discount.parse()
        self.discount_id += 1
        self.discounts[self.discount_id] = discount
        return discount

    def calculateDiscountForProduct(self, product, basket, total_price):
        total_percent = 0
        for discount in self.discounts.values():
            total_percent += discount.calculate(product, basket, total_price)
        return total_percent

    def getDiscount(self, discount_id):
        if self.discounts.get(discount_id) is None:
            raise Exception("No such discount exists")
        return self.discounts[discount_id]



