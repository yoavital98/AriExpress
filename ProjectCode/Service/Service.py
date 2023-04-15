from ProjectCode.Domain.Controllers.StoreFacade import *


class Service:
    def __init__(self):
        self.storeFacade = StoreFacade()  # activates loadData in constructor
