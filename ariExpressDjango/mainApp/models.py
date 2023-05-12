from django.db import models
from django.utils.html import format_html


class Product(models.Model):
    product_id = models.IntegerField()
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.IntegerField()
    categories = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Store(models.Model):
    store_name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product)
    active = models.BooleanField()
    # accesses = self.getAcceses(store.get_accesses())
    # bids = self.getBids(store.get_bids())
    # bids_requests = self.getBidsRequests(store.get_bids_requests())
    # auctions = self.getAuctions(store.get_auctions())
    # lotteries = self.getLotteries(store.get_lottery())

    def __str__(self):
        return self.store_name


class Cart(models.Model):
    cart_id = models.IntegerField()
    username = models.CharField(max_length=100)
    baskets = models.ForeignKey('Basket', on_delete=models.CASCADE, null=True, blank=True) # TODO: check cascade

    def __str__(self):
        return self.username
    

class Basket(models.Model):
    products = models.ManyToManyField(Product, blank=True)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    # bids = self.getBids(basket.get_bids()) #return

    def __str__(self):
        return 'Cart '+ self.cart_id + ' Store ' + self.store_id


class Member(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    # isLoggedIn = models.BooleanField()
    cart_id = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class UserMessage(models.Model):
    STATUS = (
        ('pending', 'pending'),
        ('read', 'read'),
    )
    id = models.AutoField(primary_key=True)
    sender = models.CharField(max_length=50) #probably should be changed to the member.id
    receiver = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')

    def situation(self):
        if self.status=='read':
            return format_html('<span style="color: black">{0}</span>', self.status)  
        else:
            return format_html('<span style="color: red">{0}</span>', self.status)
    situation.allow_tags = True

    def __str__(self):
        return self.sender

