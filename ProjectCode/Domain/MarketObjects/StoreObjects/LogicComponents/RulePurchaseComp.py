from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.LogicComp import LogicComp


class RulePurchaseComp(LogicComp):
    """
            rule_type := "alcohol_restriction" | to be added
            product := product_id | -1 for non-specific product rule
            category := category name | "" for non specific category rule
            user_field := age | logged in status | etc..
            operator := ">=" | "<=" | "=="
            quantity := quantity of a product | total price
    """

    def __init__(self, rule_type, product, category, user_field, operator, quantity):
        super().__init__("")
        self.rule_type = self.__validateRuleType(rule_type)
        self.product_id = product
        self.category = category
        self.user_field = user_field
        self.operator = operator
        self.quantity = quantity

    """
        basket := dict(int,int) -> (product id, quantity in basket)
    """
    def checkIfSatisfy(self, basket, total_price, user):
        if user is None: #User policies
            if self.rule_type == "product_amount":
                return self.productAmount(basket)
        elif basket is None or total_price is None: #Basket policies
            if self.rule_type == "alcohol_restriction":
                return self.alcoholRestriction(user.get_age())
        raise Exception("No such rule type exists")


    def productAmount(self, basket):
        basket_product_quantity = basket.get(self.product_id)
        if basket_product_quantity is None:
            return True
        elif self.compareWithOperator(basket_product_quantity):
            return True
        return False


    def alcoholRestriction(self, age):
        if self.user_field == "age":
            return self.compareWithOperator(age)

    def compareWithOperator(self, arg):
        if self.operator == ">=":
            return arg >= self.quantity
        elif self.operator == "<=":
            return arg <= self.quantity
        elif self.operator == "==":
            return arg == self.quantity
        else:
            raise Exception("No such operator exists")


    def __validateRuleType(self, rule_type):
        rule_types = {"product_amount":True, "alcohol_restriction":True}
        if rule_types.get(rule_type):
            return rule_type
        else:
            raise Exception("No such rule type exists")