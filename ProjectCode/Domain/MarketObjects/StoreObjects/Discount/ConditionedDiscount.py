from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.DiscountType import DiscountType
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.LogicComp import LogicComp
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.AndComp import AndComp
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.OrComp import OrComp
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.RuleComp import RuleComp
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.XorComp import XorComp


class ConditionedDiscount(DiscountType):
    """
        rule := { rule_type:= defined in RuleComp,
                 product_id: defined in RuleComp,
                 operator: defined in RuleComp,
                 quantity: defined in RuleComp,
                 child: {logic_type: "OR" | "XOR" | "AND", rule: rule} }
        logic_comp := XorComp | OrComp | AndComp | RuleComp
    """
    def __init__(self, percent, level, level_name, rule):
        super().__init__(percent, level, level_name)
        self.rule = rule
        self.logic_comp: LogicComp = None
        #self.percent = percent
        #self.level = level
        #self.level_name = level_name

    #returns price for a product after discount
    def calculate(self, product, basket, total_price, category_or_product_id):

        if super()._checkIfRelevant(category_or_product_id) and self.logic_comp.checkIfSatisfy(product, basket, total_price):
            return self.percent
        else:
            return 0


    def parse(self):
        if self.rule["child"]:
            child_type = self.rule["logic_type"]
            if child_type == "OR":
                self.logic_comp = OrComp(self.rule)
            elif child_type == "XOR":
                self.logic_comp = XorComp(self.rule)
            else:
                self.logic_comp = AndComp(self.rule)
            self.logic_comp.parse()
        else:
            self.logic_comp = RuleComp(self.rule["rule_type"], self.rule["product_id"], self.rule["operator"], self.rule["quantity"])
