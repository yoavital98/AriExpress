from ProjectCode.DAL.PurchasePolicyModel import PurchasePolicyModel
from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.Domain.MarketObjects.StoreObjects.PurchasePolicy import PurchasePolicy
from ProjectCode.Domain.Repository.Repository import Repository


class PurchasePolicyRepository(Repository):

    def __init__(self, store_name):
        self.model = PurchasePolicyModel
        self.store_name = store_name

    def __getitem__(self, policy_id):
        return self.get(policy_id)


    def __setitem__(self, key, value):
        try:
            return self.add(value)
        except Exception as e:
            raise Exception("PurchasePolicyRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("PurchasePolicyRepository: __delitem__ failed: " + str(e))

    def __contains__(self, item):
        try:
            return self.contains(item)
        except Exception as e:
            raise Exception("PurchasePolicyRepository: __contains__ failed: " + str(e))


    def get(self, pk=None):
        try:
            if pk is None:
                store_entry = StoreModel.get(StoreModel.store_name == self.store_name)
                policy_list = []
                for policy_entry in store_entry.policies:
                    policy_list.append(self.__createDomainObject(policy_entry))
                return policy_list
            else:
                policy_entry = self.model.get(self.model.policy_id == pk)
                return self.__createDomainObject(policy_entry)
        except Exception as e:
            return None

    def __createDomainObject(self, policy_entry):
        policy = None
        policy_type = policy_entry.policy_type
        if policy_type == "PurchasePolicy":
            policy = PurchasePolicy(policy_entry.level, policy_entry.level_name, policy_entry.rule, policy_id=policy_entry.policy_id)
        else:
            raise Exception("DiscountRepository: __createDomainObject failed: discount type not found")
        return policy

    def add(self, policy: PurchasePolicy):
        store_entry = StoreModel.get(StoreModel.store_name == self.store_name)
        policy_entry = self.model.create(store=store_entry, policy_type=policy.get_policy_type(), level=policy.get_level(), level_name=policy.get_level_name(), rule=policy.get_rule())
        return policy

    def remove(self, pk):
        policy_entry = self.model.get(PurchasePolicyModel.discount_id == pk)
        policy_entry.delete_instance()
        return True

    def keys(self):
        try:
            return [policy.policy_id for policy in self.model.select()]
        except Exception as e:
            return []

    def values(self):
        return self.get()

    def contains(self, policy_id: int):
        return policy_id in self.keys()