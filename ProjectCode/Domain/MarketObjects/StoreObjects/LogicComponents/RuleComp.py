from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.LogicComp import LogicComp


class RuleComp(LogicComp):

    """
        rule_type := "basket_total_price" | "amount_of_product" | "amount_of_category"
        product := product_id | -1 for non-specific product rule
        category := category name | "" for non specific category rule
        operator := ">=" | "<=" | "=="
        quantity := quantity of a product | total price
        Example: ("basket_total_price", -1, "", "==", 100)          --> basket total price equals 100 NIS.
        Example: ("amount_of_product", 2, "", ">=", 5)              --> the amount of product with product_id of 2 is greater-equals than 5
        Example: ("amount_of_category", -1, "fruit", "<=", 3)       --> the amount of product with category of "fruit" is less-equals than 3

    """
    def __init__(self, rule_type, product, operator, quantity, category):
        super().__init__("")
        self.rule_type = rule_type
        self.product_id = product
        self.category = category
        self.operator = operator
        self.quantity = int(quantity)

    def checkIfSatisfy(self, product, basket, total_price):
        # if self.category != "" and self.category not in product.get_categories():
        #     return False
        # if self.product_id != -1 and self.product_id != product.get_product_id():
        #     return False
        if self.rule_type == "basket_total_price":
            return self.basketTotalPrice(int(total_price))
        elif self.rule_type == "amount_of_product":
            return self.amoutOfProduct(basket)
        elif self.rule_type == "amount_of_category":
            return self.amountOfCategory(basket)

    #TODO: add base rules

    def amountOfCategory(self, basket):
        amount = 0
        for product_id, product_tuple in basket.items():
            cur_product, cur_quantity = product_tuple[0], product_tuple[1]
            if self.category in cur_product.get_categories():
                amount += cur_quantity
        if self.compareWithOperator(amount):
            return True
        return False

    def amoutOfProduct(self, basket):
        for product_id, product_tuple in basket.items():
            if int(product_id) == self.product_id and self.compareWithOperator(product_tuple[1]):
                return True
        return False

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