
class DataLottery:
    def __init__(self, lottery):
        self.lottery_id = lottery.get_lottery_id()
        self.product_id = lottery.get_product_id()
        self.price = lottery.get_price()
        self.accumulated_price = lottery.get_accumulated_price()
        self.participants = lottery.get_participants()
        self.winner = lottery.get_winner()