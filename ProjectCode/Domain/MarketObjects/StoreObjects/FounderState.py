from ProjectCode.Domain.MarketObjects.StoreObjects.AccessState import AccessState


class FounderState(AccessState):

    def __init__(self):
        super().__init__()
        for name, func in self.permission_names.items():
            self.permissions[name] = func


