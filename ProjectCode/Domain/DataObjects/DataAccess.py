import json


class DataAccess:
    #TODO: TO BE CHANGED!!!!!!!!!!!!!!
    def __init__(self, access):
        self.username = access.get_user().get_username()
        self.store_name = access.get_store().get_store_name()
        self.isFounder = access.isFounder
        self.isOwner = access.isOwner
        self.isManager = access.isManager
