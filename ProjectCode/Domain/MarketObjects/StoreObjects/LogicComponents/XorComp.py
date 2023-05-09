from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.LogicComp import LogicComp
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.RuleComp import RuleComp


class XorComp(LogicComp):

    def __init__(self, rule_dict):
        super().__init__(rule_dict)


    def checkIfSatisfy(self, product, basket, total_price):
        return self.right_rule.checkIfSatisfy(product, basket, total_price) ^ self.left_rule.checkIfSatisfy(product, basket, total_price)

