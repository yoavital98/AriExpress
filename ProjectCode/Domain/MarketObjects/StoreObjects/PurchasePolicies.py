from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.StoreObjects.PurchasePolicy import PurchasePolicy
from ProjectCode.Domain.Repository.PurchasePolicyRepository import PurchasePolicyRepository


class PurchasePolicies:

    def __init__(self, store_name):
        self.store_name = store_name
        self.policies = PurchasePolicyRepository(store_name)
        self.pruchase_policy_id = 0

    def addPurchasePolicy(self, **kwargs):
        policy = None
        purchase_policy, level = kwargs["purchase_policy"], kwargs["level"]
        level_value, rule = kwargs["level_name"], kwargs["rule"]
        if purchase_policy == "PurchasePolicy":
            policy = PurchasePolicy(level, level_value, rule)
        else:
            raise Exception("No such policy exists")
        self.pruchase_policy_id += 1
        self.policies[self.get_policy_id()] = policy
        policy = self.policies[self.get_policy_id()]
        return policy


    def checkAllPolicies(self, product, basket, total_price, user=None):
        print(self.policies.keys())
        print(self.policies.values())
        for policy in self.policies.values():
            if not policy.calculate(product, basket, total_price, user):
                return False
        return True

    def checkBasketPolicies(self, basket, total_price):
        for policy in self.policies.values():
            if policy.level != "User" and not policy.calculate(basket, total_price, None):
                return False
        return True

    def get_policy_id(self):
        return self.policies.get_highest_id()

    def checkUserPolicies(self, user):
        for policy in self.policies.values():
            if policy.level == "User" and not policy.calculate(None, None, user):
                return False
        return True

    def getPurchasePolicy(self, policy_id):
        return self.policies.get(policy_id)


