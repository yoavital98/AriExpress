import string

from ExternalServices import *
from MessageController import *
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.Objects import User, Store, Access
from TransactionHistory import *


class StoreFacade:
    def __init__(self):
        self.users = TypedDict(string, User)  # by id
        self.stores = TypedDict(string, Store)  # by id
        self.externalServices = ExternalServices()
        self.messageController = MessageController()
        self.transactionHistory = TransactionHistory()
        self.accesses = TypedDict(string, Access)  # optional TODO check key type
        self.loadData()

    def loadData(self):  # todo complete
        pass
