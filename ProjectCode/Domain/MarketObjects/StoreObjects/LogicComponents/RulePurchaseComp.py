from datetime import datetime

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
        self.rule_types = {"amount_of_product": True, "alcohol_restriction": True,"basket_total_price": True, "day_of_the_week": True }
        self.rule_type = self.__validateRuleType(rule_type)
        self.product_id = product
        self.category = category
        self.user_field = user_field
        self.operator = operator
        self.quantity = quantity


    """
        basket := dict(int,int) -> (product id, quantity in basket)
    """
    def checkIfSatisfy(self, product, basket, total_price, user=None):
        if user is None: #User policies
            if self.rule_type == "amount_of_product":
                return self.productAmount(basket)
            elif self.rule_type == "basket_total_price":
                return self.compareWithOperator(total_price)
            elif self.rule_type == "day_of_the_week":
                return self.dayOfTheWeek(product, basket)
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

    def dayOfTheWeek(self, product, basket):
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_day = datetime.now().weekday()
        if days_of_week[current_day] == self.user_field:
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
        if self.rule_types.get(rule_type):
            return rule_type
        else:
            raise Exception("No such rule type exists")