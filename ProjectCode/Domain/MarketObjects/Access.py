import json

from ProjectCode.Domain.Helpers.JsonSerialize import JsonSerialize
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.StoreObjects.AccessState import AccessState
from ProjectCode.Domain.MarketObjects.StoreObjects.FounderState import FounderState
from ProjectCode.Domain.MarketObjects.StoreObjects.ManagerState import ManagerState
from ProjectCode.Domain.MarketObjects.StoreObjects.OwnerState import OwnerState



class Access:

    def __init__(self, store, user, nominated_by_username):
        self.nominated_by_username = nominated_by_username
        self.nominations = TypedDict(str, Access) #username, Access
        self.user = user
        self.store = store
        self.access_state = AccessState()


    def setAccess(self, role):
        if role == "Owner":
            self.setOwner()
        elif role == "Manager":
            self.setManager()
        elif role == "Founder":
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
        if role == "Any":
            return True
        elif role == "Founder":
            return isinstance(self.access_state,FounderState)
        elif role == "Owner":
            return isinstance(self.access_state,OwnerState)
        elif role == "Manager":
            return isinstance(self.access_state,ManagerState)


    def addNominatedUsername(self, username, access):
        self.nominations[username] = access



    #------ Permission Functions -------#
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

    def canManagePolicies(self):
        return self.access_state.checkForPermission("Policies")

    def canManageDiscounts(self):
        return self.access_state.checkForPermission("Discounts")


    def removeAccessFromMember(self):
        self.user.get_accesses().pop(self.store.get_store_name())

    def get_user(self):
        return self.user

    def get_store(self):
        return self.store

    def get_access_state(self):
        return self.access_state

    def get_nominated_by_username(self):
        return self.nominated_by_username

    def get_nominations(self):
        return self.nominations

    def get_access_state_name(self):
        return type(self.access_state).__name__[:-5]


    # =======================JSON=======================#
    def toJson(self):
        data = {
            'user': self.user,
            'store': self.store,
            'nominated_by_username': self.nominated_by_username,
            'nominations': JsonSerialize.toJsonAttributes(self.nominations),
            'access_state': self.access_state.toJson()
        }
        return json.dumps(data)

