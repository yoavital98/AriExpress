from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.LogicComp import LogicComp


class AndComp(LogicComp):

    def __init__(self, rule_dict):
        super().__init__(rule_dict)


    def checkIfSatisfy(self, product, basket, total_price):
        return self.left_rule.checkIfSatisfy(product, basket, total_price) and self.right_rule.checkIfSatisfy(product, basket, total_price)
