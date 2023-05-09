from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.LogicComp import LogicComp


class RuleComp(LogicComp):

    """
        rule_type := "basket_total_price" | to be added
        product := product_id | -1 for non-specific product rule
        operator := ">=" | "<=" | "=="
        quantity := quantity or total price

        Example: ("basket_total_price", -1, "==", 100) --> basket total price equals 100 NIS.

    """
    def __init__(self, rule_type, product, operator, quantity):
        self.rule_type = rule_type
        self.product = product
        self.operator = operator
        self.quantity = quantity

    def checkIfSatisfy(self, product, basket, total_price):
        if self.rule_type == "basket_total_price":
            return self.basketTotalPrice(total_price)



    def basketTotalPrice(self, total_price):
        return self.compareWithOperator(total_price)

    def compareWithOperator(self, arg):
        if self.operator == ">=":
            return arg >= self.quantity
        elif self.operator == "<=":
            return arg <= self.quantity
        elif self.operator == "==":
            return arg == self.quantity
        else:
            raise Exception("No such operator exists")