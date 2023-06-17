from ProjectCode.Domain.Helpers.JsonSerialize import JsonSerialize
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.AddComp import AddComp
from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.ConditionedDiscount import ConditionedDiscount
from ProjectCode.Domain.MarketObjects.StoreObjects.Policy import Policy
from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.SimpleDiscount import SimpleDiscount
from ProjectCode.Domain.Repository.DiscountRepository import DiscountRepository


class DiscountPolicy:

    # IMPORTANT!!: only root discount have an ID
    # for example: child of Add discount wont have an ID
    def __init__(self, store_name):
        #backup
        # self.discounts = TypedDict(int, Policy)  #(discountId, disType)
        # self.discount_id = 0
        # self.store_name = store_name

        self.discounts = DiscountRepository(store_name)  # (discountId, disType)
        self.discount_id = 0
        self.store_name = store_name

        # ORM FIRLEDS --- TO BE REPLACED

        # self.discounts_test = DiscountRepository(store_name)
    """
        kwargs := 
            discount_type := Conditioned | Simple | Coupon | Max | Add
            percent := 1-100 int value
            level := "Store" | "Category" | "Product"
            level_name := product_id | category name | "" blank for store
            rule := RuleComp (optional)
            discounts := Dict(str, Policy)
            Example: {"1": {"discount_type": "Simple" ....}, "2": {"discount_type": "Coupon"...} }
    """

    #TODO: add validation for kwargs fields to each discount type
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
            if percent < 1 or percent > 100:
                raise Exception("discount percentage can be only within 1-100")
            discount = SimpleDiscount(percent, level, level_name)
        elif discount_type == "Coupon": #TODO: impl coupon discount
            pass
        else:
            raise Exception("No such discount type exists")
        #discount.parse() -- orm change
        self.discount_id += 1
        self.discounts[self.discount_id] = discount
        return discount

    def calculateDiscountForProduct(self, product, basket, total_price):
        total_percent = 0
        for discount in self.discounts.values():
            total_percent += discount.calculate(product, basket, total_price)
        return total_percent

    def getDiscount(self, discount_id):
        if self.discounts[discount_id] is None:
            raise Exception("No such discount exists")
        return self.discounts[discount_id]

    def getAllDiscounts(self):
        return self.discounts

    # =======================JSON=======================#

    def toJson(self):
        return {
            "discounts": JsonSerialize.toJsonAttributes(self.discounts)
        }
    # =======================FOR TESTS=======================#

    def calculateOverallDiscountsForSimple(self):
        total_discount = 0
        for discount in self.discounts.values():
            total_discount += discount.calculateForTest()
        return total_discount