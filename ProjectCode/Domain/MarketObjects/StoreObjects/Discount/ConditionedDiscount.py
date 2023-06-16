from ProjectCode.Domain.MarketObjects.StoreObjects.Policy import Policy
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.LogicComp import LogicComp
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.LogicUnit import LogicUnit
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.RuleComp import RuleComp


class ConditionedDiscount(Policy):
    """
        rule := { rule_type:= defined in RuleComp,
                 product_id: defined in RuleComp,
                 operator: defined in RuleComp,
                 quantity: defined in RuleComp,
                 category: defined in RuleComp,
                 child: {logic_type: "OR" | "XOR" | "AND", rule: rule} }
        logic_comp := LogicUnit | RuleComp
    """
    def __init__(self, percent, level, level_name, rule, discount_id=-1):
        super().__init__(level, level_name)
        self.discount_id = discount_id
        self.rule = rule
        self.percent = percent
        self.logic_comp: LogicComp = None
        self.parse()
        #self.percent = percent
        #self.level = level
        #self.level_name = level_name


    def __str__(self):
        return "ConditionedDiscount: " + str(self.percent) + "% off " + str(self.level) + " " + str(self.level_name) + " if " + str(self.rule)

    #returns price for a product after discount
    def calculate(self, product, basket, total_price): #TODO: check here
        if self.level == "Category" and self.level_name not in product.get_categories():
            return 0
        elif self.level == "Product" and int(self.level_name) != product.get_product_id():
            return 0
        if self.logic_comp.checkIfSatisfy(product, basket, total_price):
            return self.percent
        else:
            return 0


    def parse(self):
        if self.rule["child"]:
            child_type = self.rule["child"]["logic_type"]
            self.logic_comp = LogicUnit(self.rule, child_type)
            self.logic_comp.parse()
        else:
            self.logic_comp = RuleComp(self.rule["rule_type"], self.rule["product_id"], self.rule["operator"], self.rule["quantity"], self.rule["category"])

    def get_discount_id(self):
        return self.discount_id

    def get_discount_type(self):
        return "Conditioned"

    def get_percent(self):
        return self.percent

    def get_level(self):
        return self.level

    def get_level_name(self):
        return self.level_name

    def get_rule(self):
        return self.rule

    def get_discount_dict(self):
        return {}

    # =======================JSON=======================#

    def toJson(self):
        return{
            "percent": self.percent,
            "level": self.level,
            "level_name": self.level_name,
            "rule": self.rule,
            "discount_type": "Conditioned"
        }