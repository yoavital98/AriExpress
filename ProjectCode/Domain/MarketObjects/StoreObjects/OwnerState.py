
from ProjectCode.Domain.MarketObjects.StoreObjects.AccessState import AccessState


class OwnerState(AccessState):

    def __init__(self):
        super().__init__()
        self.permissions["ProductChange"] = self.permission_names["ProductChange"]
        self.permissions["Bid"] = self.permission_names["Bid"]



