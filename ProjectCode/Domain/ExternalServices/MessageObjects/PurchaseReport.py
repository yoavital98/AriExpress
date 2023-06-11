class PurchaseReport:
    def __init__(self, username, storename, productTuples, totalPayment):
        self.username = username
        self.storename = storename
        self.productTuples = productTuples
        self.totalBasketPayment = totalPayment

    def getUsername(self):
        return self.username

    def getStorename(self):
        return self.storename

    def getProducts(self):
        return self.productTuples

    def getTotalBasketPayment(self):
        return self.totalBasketPayment

    def toJson(self):
        product_dicts = [{"productId": p[0], "productname": p[1], "quantity": p[2], "price4unit": p[3]} for p in
                         self.productTuples]
        return {
            "username": self.username,
            "storename": self.storename,
            "totalBasketPayment": self.totalBasketPayment,
            "productTuples": product_dicts
        }
