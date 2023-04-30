class Access:

    def __init__(self, store, user):
        self.user = user
        self.store = store
        self.isManager = False
        self.isFounder = False
        self.isOwner = False

    def setOwner(self, flag):
        self.isOwner = flag

    def setFounder(self, flag):
        self.isFounder = flag

    def setManager(self, flag):
        self.isManager = flag

    def get_user(self):
        return self.user

    def get_store(self):
        return self.store
