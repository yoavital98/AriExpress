from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.StoreObjects.AccessState import AccessState
from ProjectCode.Domain.MarketObjects.StoreObjects.FounderState import FounderState
from ProjectCode.Domain.MarketObjects.StoreObjects.ManagerState import ManagerState
from ProjectCode.Domain.MarketObjects.StoreObjects.OwnerState import OwnerState


class Access:

    def __init__(self, store, user, nominated_by_username):
        self.nominated_by_username = nominated_by_username
        self.nominations = TypedDict(str,str) #storename, username
        self.user = user
        self.store = store
        self.access_state = AccessState()


    def setAccess(self, role):
        if role is "Owner":
            self.setOwner()
        elif role is "Manager":
            self.setOwner()
        elif role is "Founder":
            self.setFounder()
        else:
            raise Exception("No such role exists.")


    def setOwner(self):
        self.access_state = OwnerState()

    def setFounder(self):
        self.access_state = FounderState()

    def setManager(self):
        self.access_state = ManagerState()


    def hasRole(self, role="Any"):
        if role is "Any":
            return True
        elif role is "Founder":
            return isinstance(self.access_state,FounderState)
        elif role is "Owner":
            return isinstance(self.access_state,OwnerState)
        elif role is "Manager":
            return isinstance(self.access_state,ManagerState)

    def getAccessState(self):
        return type(self.access_state).__name__[:-5]

    def addNominatedUsername(self, username, storename):
        self.nominations[storename] = username

    def canModifyPermissions(self):
        return self.access_state.checkForPermission("ModifyPermissions")

    def canChangeProducts(self):
        return self.access_state.checkForPermission("ProductChange")

    def canManageBids(self):
        return self.access_state.checkForPermission("Bid")

    def canManageAuctions(self):
        return self.access_state.checkForPermission("Auction")

    def canManageLottery(self):
        return self.access_state.checkForPermission("Lottery")

    def canChangeStatus(self):
        return self.access_state.checkForPermission("StatusChange")

    def canViewStaffInformation(self):
        return self.access_state.checkForPermission("StaffInfo")

    def get_user(self):
        return self.user

    def get_store(self):
        return self.store


