from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.LogicComp import LogicComp
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.RulePurchaseComp import RulePurchaseComp


class LogicPurchaseUnit(LogicComp):

    """
        rule_dict := RulePurchaseComp
        logic_type := "CONDITION" | "OR" | "AND"
    """
    def __init__(self, rule_dict, logic_type):
        super().__init__(rule_dict)
        if logic_type == "CONDITION" or logic_type == "OR" or logic_type == "AND":
            self.logic_type = logic_type
        else:
            raise Exception("No such logic operator exists")


    def checkIfSatisfy(self, product, basket, total_price, user=None):
        satisfy_left = self.left_rule.checkIfSatisfy(product, basket, total_price, user=user)
        satisfy_right = self.right_rule.checkIfSatisfy(product, basket, total_price, user=user)
        if self.logic_type == "OR":
            return satisfy_right or satisfy_left
        elif self.logic_type == "AND":
            return satisfy_right and satisfy_left
        elif self.logic_type == "CONDITION":
            if satisfy_right:
                return satisfy_left
        return False

    def parse(self):
        #self._validateRuleArguments()
        self.left_rule = RulePurchaseComp(self.rule["rule_type"], self.rule["product_id"],
                                         self.rule["category"], self.rule["user_field"],
                                         self.rule["operator"], self.rule["quantity"])

        if self.rule["child"]["rule"]["child"]:
            child_rule = self.rule["child"]["rule"]
            child_type = child_rule["child"]["rule"]["child"]["logic_type"]
            self.right_rule = LogicPurchaseUnit(child_rule, child_type)
            self.right_rule.parse()
        else:
            child_rule = self.rule["child"]["rule"]
            self.right_rule = RulePurchaseComp(child_rule["rule_type"], child_rule["product_id"],
                                         child_rule["category"], child_rule["user_field"],
                                         child_rule["operator"], child_rule["quantity"])

