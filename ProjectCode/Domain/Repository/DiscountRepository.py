from ProjectCode.DAL.DiscountModel import DiscountModel
from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.AddComp import AddComp
from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.ConditionedDiscount import ConditionedDiscount
from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.SimpleDiscount import SimpleDiscount
from ProjectCode.Domain.Repository.Repository import Repository


class DiscountRepository(Repository):

    def __init__(self, store_name):
        self.model = DiscountModel
        self.store_name = store_name

    def __getitem__(self, discount_id):
        return self.get(discount_id)


    def __setitem__(self, key, value): #key is meaningless
        try:
            return self.add(value)
        except Exception as e:
            raise Exception("DiscountRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("DiscountRepository: __delitem__ failed: " + str(e))

    def __contains__(self, item):
        try:
            return self.contains(item)
        except Exception as e:
            raise Exception("DiscountRepository: __contains__ failed: " + str(e))


    def get(self, pk=None):
        try:
            if pk is None:
                store_entry = StoreModel.get(StoreModel.store_name == self.store_name)
                discount_list = []
                for discount_entry in store_entry.discounts:
                    discount_list.append(self.__createDomainObject(discount_entry))
                return discount_list
            else:
                discount_entry = self.model.get(self.model.discount_id == pk)
                return self.__createDomainObject(discount_entry)
        except Exception as e:
            return None

    def __createDomainObject(self, discount_entry):
        discount = None
        discount_type = discount_entry.discount_type
        if discount_type == "Conditioned":
            discount = ConditionedDiscount(discount_entry.percent, discount_entry.level, discount_entry.level_name, discount_entry.rule, discount_id=discount_entry.discount_id)
        elif discount_type == "Simple":
            discount = SimpleDiscount(discount_entry.percent, discount_entry.level, discount_entry.level_name, discount_id=discount_entry.discount_id)
        elif discount_type == "Coupon":
            pass
        elif discount_type == "Max":
            pass
        elif discount_type == "Add":
            discount = AddComp(discount_entry.discount_dict, discount_id=discount_entry.discount_id)
        else:
            raise Exception("DiscountRepository: __createDomainObject failed: discount type not found")
        return discount

    def add(self, discount):
        store_entry = StoreModel.get(StoreModel.store_name == self.store_name)
        discount_entry = self.model.create(store=store_entry, discount_type=discount.get_discount_type(), percent=discount.get_percent(), level=discount.get_level(), level_name=discount.get_level_name(), rule=discount.get_rule(), discount_dict=discount.get_discount_dict())
        return discount

    def remove(self, pk):
        discount_entry = DiscountModel.get(DiscountModel.discount_id == pk)
        discount_entry.delete_instance()
        return True

    def keys(self):
        try:
            return [discount.discount_id for discount in DiscountModel.select()]
        except Exception as e:
            return []

    def values(self):
        return self.get()

    def contains(self, discount_id):
        return discount_id in self.keys()