from abc import ABC, abstractmethod

from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.AndComp import AndComp
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.OrComp import OrComp
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.RuleComp import RuleComp
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.XorComp import XorComp


class LogicComp(ABC):

    """
        EXAMPLES:

        rule1 := {rule_type:"basket_total_price", product_id: "-1", operator: ">=", quantity: 100, child: {logic_type: "OR", rule: rule2} }
        translates to --> total price of the basket is atleast 100 NIS.

        rule2 := {rule_type:"product_amount", product_id: "5", operator: "=", quantity: 5, child: {} }
        translates to --> basket needs to have 5 bananas (product_id = 5 -> banana).

    """

    def __init__(self, rule_dict):
        self.rule = rule_dict
        self.left_rule: LogicComp = None
        self.right_rule: LogicComp = None

    @abstractmethod
    def checkIfSatisfy(self, product, basket, total_price):
        pass


    def parse(self):
        self.__validateRuleArguments()
        self.left_rule = RuleComp(self.rule["rule_type"], self.rule["product_id"],
                                  self.rule["operator"], self.rule["quantity"])
        child_rule = self.rule["child"]["rule"]
        if child_rule["child"]:
            child_type = child_rule["child"]["logic_type"]
            if child_type == "OR":
                self.right_rule = OrComp(child_rule)
            elif child_type == "XOR":
                self.right_rule = XorComp(child_rule)
            else:
                self.right_rule = AndComp(child_rule)
            self.right_rule.parse()
        else:
            self.right_rule = RuleComp(child_rule["rule_type"], child_rule["product_id"],
                                       child_rule["operator"], child_rule["quantity"])


    def __validateRuleArguments(self):
        if self.rule.get("rule_type") is None or self.rule.get("product_id") is None or self.rule.get("operator") is None or self.rule.get("quantity") is None:
            raise Exception("Missing arguments for adding a rule")
        if self.rule.get("child"):
            child_rule = self.rule.get("child").get("rule")
            if child_rule.get("rule_type") is None or child_rule.get("product_id") is None or child_rule.get("operator") is None or child_rule.get("quantity") is None:
                raise Exception("Missing arguments for adding a rule")
