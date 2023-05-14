from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    # store = models.ForeignKey('Store', on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    categories = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    store_name = models.CharField(primary_key=True, max_length=100)
    #product = models.ManyToManyField(Product)
    active = models.BooleanField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    # accesses = self.getAcceses(store.get_accesses())
    # bids = self.getBids(store.get_bids())
    # bids_requests = self.getBidsRequests(store.get_bids_requests())
    # auctions = self.getAuctions(store.get_auctions())
    # lotteries = self.getLotteries(store.get_lottery())

    def __str__(self):
        return self.store_name

# class StoreProduct(models.Model):
#     store = models.ForeignKey(Store, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     price = models.IntegerField()
#     categories = models.CharField(max_length=100)

#     def __str__(self):
#         return self.store + ', ' + self.product


# class Basket(models.Model):
#     store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
#     #products = models.ManyToManyField(Product, blank=True)
#     #cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     # bids = self.getBids(basket.get_bids()) #return
#     basket_name = models.CharField(max_length=100, null=True)
#     def __str__(self):
#         return 'Cart'
#
#
# class Cart(models.Model):
#     cart_id = models.IntegerField()
#     username = models.CharField(max_length=100)
#     baskets = models.ForeignKey(Basket, on_delete=models.CASCADE, null=True, blank=True) # TODO: check cascade
#
#     def __str__(self):
#         return self.username
#
#
#
#
# class Member(models.Model):
#     username = models.CharField(max_length=100)
#     email = models.CharField(max_length=100)
#     # isLoggedIn = models.BooleanField()
#     cart_id = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
#     password = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.username
#
#
