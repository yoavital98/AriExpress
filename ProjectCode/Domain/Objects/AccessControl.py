class AccessControl:

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
