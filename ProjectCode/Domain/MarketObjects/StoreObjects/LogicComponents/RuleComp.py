from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.LogicComp import LogicComp


class RuleComp(LogicComp):

    """
        rule_type := "basket_total_price" | to be added
        product := product_id | -1 for non-specific product rule
        category := category name | "" for non specific category rule
        operator := ">=" | "<=" | "=="
        quantity := quantity of a product | total price
        Example: ("basket_total_price", -1, "==", 100) --> basket total price equals 100 NIS.

    """
    def __init__(self, rule_type, product, operator, quantity, category):
        super().__init__("")
        self.rule_type = rule_type
        self.product_id = product
        self.category = category
        self.operator = operator
        self.quantity = quantity

    def checkIfSatisfy(self, product, basket, total_price):
        if self.category != "" and self.category not in product.get_categories():
            return False
        if self.product_id != -1 and self.product_id != product.get_product_id():
            return False
        if self.rule_type == "basket_total_price":
            return self.basketTotalPrice(total_price)
        elif self.rule_type == "amount_of_product":
            return self.amoutOfProduct(basket[product.get_product_id()])

    #TODO: add base rules

    def amoutOfProduct(self, amount):
        return self.compareWithOperator(amount)

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