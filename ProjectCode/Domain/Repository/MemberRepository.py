from peewee import *

from ProjectCode.DAL.BasketModel import BasketModel
#from ProjectCode.DAL.CartModel import CartModel
from ProjectCode.DAL.MemberModel import MemberModel
from ProjectCode.DAL.ProductBasketModel import ProductBasketModel
from ProjectCode.DAL.ProductModel import ProductModel
from ProjectCode.Domain.MarketObjects.Basket import Basket
from ProjectCode.Domain.MarketObjects.Cart import Cart
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product
from ProjectCode.Domain.MarketObjects.UserObjects.Member import Member
from ProjectCode.Domain.Repository.BasketRepository import BasketRepository
from ProjectCode.Domain.Repository.Repository import Repository


class MemberRepository(Repository):

    def __init__(self):
        self.model = MemberModel

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
                member_list.append(Member(-1, entry.user_name, entry.password, entry.email))

            return member_list
        else:
            entry = self.model.get(self.model.user_name == pk)
            member_obj = Member(-1, entry.user_name, entry.password, entry.email)
            return member_obj

    def add(self, member: Member):
        member_entry = self.model.create(user_name=member.get_username(), password=member.get_password() ,email=member.get_email())
        return member

    def remove(self, pk):
        user_entry = MemberModel.get(MemberModel.user_name == pk)
        user_entry.cart.delete_instance()
        user_entry.delete_instance()

    def keys(self):
        return [member.user_name for member in MemberModel.select()]

    def values(self):
        return self.get()

    def getCart(self, user_name):
        # Create an empty cart
        cart = Cart(user_name)

        # Get the basket entries for the given user_name
        basket_entries = BasketModel.select().where(BasketModel.user_name == user_name)

        for basket_entry in basket_entries:

            basket = Basket(basket_entry.user_name, basket_entry.store)

            # get the product entries for the current basket
            product_entries = (
                ProductBasketModel.select()
                .join(ProductModel)
                .where(
                    ProductBasketModel.basket == basket_entry,
                    ProductModel.store == basket_entry.store
                )
            )

            for product_entry in product_entries:
                product = Product(
                    product_entry.product_model.product_id,
                    product_entry.product_model.name,
                    product_entry.product_model.quantity,  # Use quantity from ProductModel
                    product_entry.product_model.price,
                    product_entry.product_model.categories
                )

                # Add the product to the basket with the quantity from the ProductBasketModel
                basket.add_Product(product_entry.product_id, product, product_entry.quantity)

            cart.baskets[basket_entry.store.store_name] = basket

        return cart
