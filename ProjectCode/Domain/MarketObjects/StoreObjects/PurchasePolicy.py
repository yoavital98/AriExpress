from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.LogicComp import LogicComp
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.LogicPurchaseUnit import LogicPurchaseUnit
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.RulePurchaseComp import RulePurchaseComp
from ProjectCode.Domain.MarketObjects.StoreObjects.Policy import Policy
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product


class PurchasePolicy(Policy):

    """
        level := Product | Category | User | Basket
        level_value := product_id | category name | user field | dict(product_id, quantity)
        rule := { rule_type:= defined in RulePurchaseComp,
                 product_id: defined in RulePurchaseComp,
                 operator: defined in RulePurchaseComp,
                 quantity: defined in RulePurchaseComp,
                 category: defined in RulePurchaseComp,
                 user_field: defined in RulePurchaseComp,
                 child: {logic_type: "OR" | "Condition" | "AND", rule: rule} }
        logic_comp := LogicPurchaseUnit | RulePurchaseComp
    """

    def __init__(self, level, level_value, rule, policy_id=-1):
        super().__init__(level, level_value)
        self.policy_id = policy_id
        self.rule = rule
        self.logic_comp: LogicComp = None
        self.parse()

    def __eq__(self, other):
        return self.get_policy_id() == other.get_policy_id()

    def calculate(self, product, basket, additional_value, user=None):
        if self.checkIfRelevant(product, user):
            return self.logic_comp.checkIfSatisfy(product, basket, additional_value)
        return True #if not relevant, then it is satisfied


    def checkIfRelevant(self, product: Product, user):
        if self.level == "Category":
            return self.level_name in product.get_categories()
        elif self.level == "Product":
            return self.level_name == product.get_product_id()
        elif self.level == "Basket" or hasattr(user, self.level_name):
            return True
        return False



    def parse(self):
        if self.rule["child"]:
            child_type = self.rule["child"]["logic_type"]
            self.logic_comp = LogicPurchaseUnit(self.rule, child_type)
            self.logic_comp.parse()
        else:
            self.logic_comp = RulePurchaseComp(self.rule["rule_type"], self.rule["product_id"],
                                               self.rule["category"], self.rule["user_field"],
                                               self.rule["operator"], self.rule["quantity"])



    def get_policy_id(self):
        return self.policy_id

    def get_policy_type(self):
        return "PurchasePolicy"

    def get_level(self):
        return self.level

    def get_level_name(self):
        return self.level_name

    def get_rule(self):
        return self.rule
