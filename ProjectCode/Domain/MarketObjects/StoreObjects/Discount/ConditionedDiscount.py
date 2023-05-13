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
    def __init__(self, percent, level, level_name, rule):
        super().__init__(level, level_name)
        self.rule = rule
        self.percent = percent
        self.logic_comp: LogicComp = None
        #self.percent = percent
        #self.level = level
        #self.level_name = level_name

    #returns price for a product after discount
    def calculate(self, product, basket, total_price):
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

    # =======================JSON=======================#

    def toJson(self):
        return{
            "percent": self.percent,
            "level": self.level,
            "level_name": self.level_name,
            "rule": self.rule,
            "discount_type": "Conditioned"
        }