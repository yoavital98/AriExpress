from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.LogicComp import LogicComp
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.RuleComp import RuleComp


class LogicUnit(LogicComp):

    def __init__(self, rule_dict, logic_type):
        super().__init__(rule_dict)
        if logic_type == "XOR" or logic_type == "OR" or logic_type == "AND":
            self.logic_type = logic_type
        else:
            raise Exception("No such logic operator exists")

    def checkIfSatisfy(self, product, basket, total_price):
        satisfy_left = self.left_rule.checkIfSatisfy(product, basket, total_price)
        satisfy_right = self.right_rule.checkIfSatisfy(product, basket, total_price)
        if self.logic_type == "OR":
            return satisfy_right or satisfy_left
        elif self.logic_type == "AND":
            return satisfy_right and satisfy_left
        elif self.logic_type == "XOR":
            return satisfy_right ^ satisfy_left
        return False

    def parse(self):
        self._validateRuleArguments()
        self.left_rule = RuleComp(self.rule["rule_type"], self.rule["product_id"],
                                  self.rule["operator"], self.rule["quantity"], self.rule["category"])

        if len(self.rule["child"]["rule"]["child"].values()) != 0:
            child_rule = self.rule["child"]["rule"]
            child_type = child_rule["child"]["logic_type"]
            self.right_rule = LogicUnit(child_rule, child_type)
            self.right_rule.parse()
        else:
            child_rule = self.rule["child"]["rule"]
            self.right_rule = RuleComp(child_rule["rule_type"], child_rule["product_id"],
                                       child_rule["operator"], child_rule["quantity"], self.rule["category"])

