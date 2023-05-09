from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.DiscountType import DiscountType


class AddComp(DiscountType):
    def __init__(self, percent, level, level_name):
        super().__init__(percent, level, level_name)
        self.childs = list()

    # child: DiscountType
    def addChild(self, child):
        self.childs.append(child)

    def calculate(self, product, basket, total_price, category_or_product_id):
        added_percent = 0
        for child in self.childs:
            if child._checkIfRelevant(category_or_product_id):
                added_percent += child.calculate(product, basket, total_price, category_or_product_id)
        return added_percent


    #TODO: add parser