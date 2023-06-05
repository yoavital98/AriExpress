from peewee import *

from ProjectCode.DAL.BasketModel import BasketModel
from ProjectCode.DAL.CartModel import CartModel
from ProjectCode.DAL.ProductBasketModel import ProductBasketModel
from ProjectCode.DAL.ProductModel import ProductModel
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.Basket import Basket
from ProjectCode.Domain.MarketObjects.Cart import Cart
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product
from ProjectCode.Domain.Repository.Repository import Repository


class CartRepository(Repository):

    def __init__(self):
        self.model = CartModel

    def __getitem__(self, user_name):
        try:
            return self.get(user_name)
        except Exception as e:
            raise Exception("CartRepository: __getitem__ failed: " + str(e))

    def __setitem__(self, key, value): #key is meaningless
        try:
            return self.add(value)
        except Exception as e:
            raise Exception("CartRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("CartRepository: __delitem__ failed: " + str(e))

    def __contains__(self, item):
         pass


    def get(self, pk=None):
        if pk is None:
            cart_list = []
            for cart_entry in self.model.select():
                cart = Cart(cart_entry.user_name)
                for basket_entry in cart_entry.baskets:
                    basket = Basket(basket_entry.user_name, basket_entry.store_name)
                    for product_basket_entry in basket_entry.products:
                        product_entry = product_basket_entry.product
                        product = Product(
                            product_entry.product_id,
                            product_entry.name,
                            product_basket_entry.quantity,
                            product_entry.price,
                            product_entry.categories
                        )
                        basket.products[product.product_id] = (
                            product,
                            product_basket_entry.quantity,
                            product_entry.price
                        )
                    cart.baskets[basket_entry.store_name] = basket
                cart_list.append(cart)
            return cart_list
        else:
            cart_entry = self.model.get(user_name=pk)
            cart = Cart(cart_entry.user_name)
            for basket_entry in cart_entry.baskets:
                #todo: storename isnt right here, it should be the store itself
                basket = Basket(basket_entry.user_name, basket_entry.store_name)
                for product_basket_entry in basket_entry.products:
                    product_entry = product_basket_entry.product
                    product = Product(
                        product_entry.product_id,
                        product_entry.name,
                        product_basket_entry.quantity,
                        product_entry.price,
                        product_entry.categories
                    )
                    basket.products[product.product_id] = (
                        product,
                        product_basket_entry.quantity,
                        product_entry.price
                    )
                cart.baskets[basket_entry.store_name] = basket
            return cart



    def add(self, cart: Cart):
        cart_entry = self.model.create(user_name=cart.username)
        for basket_key, basket in cart.baskets.items():
            basket_entry = BasketModel.create(user_name=basket.username, store_name=basket.store)
            for product_id, product_info in basket.products.items():
                product = product_info[0]  # product object
                quantity = product_info[1]
                product_entry = ProductModel.create(
                    product_id=product.product_id,
                    name=product.name,
                    quantity=quantity,
                    price=product.price,
                    categories=product.categories
                )
                ProductBasketModel.create(quantity=quantity, product=product_entry, basket=basket_entry)
            cart_entry.baskets.add(basket_entry)
        return True

    def remove(self, pk):
        cart_entry = self.model.get(user_name=pk)
        cart_entry.delete_instance(recursive=True)
        return True


    def keys(self):
        return [cart.user_name for cart in CartModel.select()]

    def values(self):
        return self.get()
