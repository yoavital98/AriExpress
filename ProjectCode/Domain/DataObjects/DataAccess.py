

class DataAccess:
    #TODO: TO BE CHANGED!!!!!!!!!!!!!!
    def __init__(self, access):
        self.username = access.get_user().get_username()
        self.store_name = access.get_store().get_store_name()
        self.isFounder = access.hasRole("Founder")
        self.isOwner = access.hasRole("Owner")
        self.isManager = access.hasRole("Manager")