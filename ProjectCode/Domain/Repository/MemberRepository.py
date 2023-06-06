from peewee import *

#from ProjectCode.DAL.BasketModel import BasketModel
#from ProjectCode.DAL.CartModel import CartModel
from ProjectCode.DAL.MemberModel import MemberModel
# from ProjectCode.DAL.ProductBasketModel import ProductBasketModel
# from ProjectCode.DAL.ProductModel import ProductModel
# from ProjectCode.Domain.MarketObjects.Basket import Basket
# from ProjectCode.Domain.MarketObjects.Cart import Cart
# from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product
from ProjectCode.Domain.MarketObjects.UserObjects.Member import Member
# from ProjectCode.Domain.Repository.BasketRepository import BasketRepository
from ProjectCode.Domain.Repository.Repository import Repository


class MemberRepository(Repository):

    def __init__(self, online=False, banned=False):
        self.model = MemberModel
        self.online = online
        self.banned = banned

    def __getitem__(self, user_name):
        try:
            return self.get(user_name)
        except Exception as e:
            raise Exception("MemberRepository: __getitem__ failed: " + str(e))

    def __setitem__(self, key, value): #key is meaningless
        try:
            return self.add(value)
        except Exception as e:
            raise Exception("MemberRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("MemberRepository: __delitem__ failed: " + str(e))

    def __contains__(self, item):
         pass

    def get(self, pk=None):
        if not pk:
            member_list = []
            for entry in self.model.select():
                member = self.__get_by_flag(entry)
                if member is not None:
                    member_list.append(member)
            return member_list
        else:
            entry = self.model.get(self.model.user_name == pk)
            member_obj = self.__get_by_flag(entry)
            return member_obj

    def __get_by_flag(self, entry):
        if self.banned and not entry.banned:
            return None
        elif self.online and not entry.logged_in:
            return None
        return Member(-1, entry.user_name, entry.password, entry.email)

    def add(self, member: Member):
        member_entry = self.model.get_or_none(self.model.user_name == member.get_username())
        if member_entry is not None:
            #update
            if self.banned:
                member_entry.banned = True
            if self.online:
                member_entry.logged_in = True
            member_entry.password = member.get_password()
            member_entry.email = member.get_email()
            member_entry.save()
        else:
            #create
            member_entry = self.model.create(user_name=member.get_username(), password=member.get_password() ,email=member.get_email())
        return member

    def remove(self, pk):
        user_entry = MemberModel.get(MemberModel.user_name == pk)
        if self.banned:
            user_entry.banned = False
            user_entry.save()
        elif self.online:
            user_entry.logged_in = False
            user_entry.save()
        else:
            user_entry.delete_instance()
        return True

    def keys(self):
        return [member.user_name for member in MemberModel.select()]

    def values(self):
        return self.get()

    def contains(self, username):
        query = None
        if self.banned:
            query = self.model.select().where(self.model.user_name == username, self.model.banned == True)
        elif self.online:
            query = self.model.select().where(self.model.user_name == username, self.model.logged_in == True)
        else:
            query = self.model.select().where(self.model.store.user_name == username)
        return query.exists()


    # def getCart(self, user_name):
    #     # Create an empty cart
    #     cart = Cart(user_name)
    #
    #     # Get the basket entries for the given user_name
    #     basket_entries = BasketModel.select().where(BasketModel.user_name == user_name)
    #
    #     for basket_entry in basket_entries:
    #
    #         basket = Basket(basket_entry.user_name, basket_entry.store)
    #
    #         # get the product entries for the current basket
    #         product_entries = (
    #             ProductBasketModel.select()
    #             .join(ProductModel)
    #             .where(
    #                 ProductBasketModel.basket == basket_entry,
    #                 ProductModel.store == basket_entry.store
    #             )
    #         )
    #
    #         for product_entry in product_entries:
    #             product = Product(
    #                 product_entry.product_model.product_id,
    #                 product_entry.product_model.name,
    #                 product_entry.product_model.quantity,  # Use quantity from ProductModel
    #                 product_entry.product_model.price,
    #                 product_entry.product_model.categories
    #             )
    #
    #             # Add the product to the basket with the quantity from the ProductBasketModel
    #             basket.add_Product(product_entry.product_id, product, product_entry.quantity)
    #
    #         cart.baskets[basket_entry.store.store_name] = basket
    #
    #     return cart
