from abc import ABC, abstractmethod




class LogicComp(ABC):

    """
        EXAMPLES:

        rule1 := {rule_type:"basket_total_price", product_id: "-1", operator: ">=", quantity: 100, child: {logic_type: "OR", rule: rule2} }
        translates to --> total price of the basket is at least 100 NIS.

        rule2 := {rule_type:"product_amount", product_id: "5", operator: "=", quantity: 5, child: {} }
        translates to --> basket needs to have 5 bananas (product_id = 5 -> banana).

    """

    def __init__(self, rule_dict):
        self.rule = rule_dict
        self.left_rule: LogicComp = None
        self.right_rule: LogicComp = None
        self.logic_type = "Rule"

    @abstractmethod
    def checkIfSatisfy(self, product, basket, total_price):
        pass

    def _validateRuleArguments(self):
        if self.rule.get("rule_type") is None or self.rule.get("product_id") is None or self.rule.get("operator") is None or self.rule.get("quantity") is None:
            raise Exception("Missing arguments for adding a rule")
        if self.rule.get("child"):
            child_rule = self.rule.get("child").get("rule")
            if child_rule.get("rule_type") is None or child_rule.get("product_id") is None or child_rule.get("operator") is None or child_rule.get("quantity") is None:
                raise Exception("Missing arguments for adding a rule")
