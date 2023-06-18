from ProjectCode.Domain.MarketObjects.StoreObjects.Policy import Policy


class SecretDiscount(Policy):


    def __init__(self, percent, level, level_name, code, discount_id=-1):
        super().__init__(level, level_name)
        self.discount_id: int = discount_id
        self.percent: int = percent
        self.code: str = code

    def calculate(self, product, basket, code):
        pass

    # =======================JSON=======================#

    def toJson(self):
        return{
            "percent": self.percent,
            "level": self.level,
            "level_name": self.level_name,
            "code": self.code,
            "discount_type": "Secret"
        }