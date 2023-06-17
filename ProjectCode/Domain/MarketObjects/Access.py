import json

from ProjectCode.Domain.Helpers.JsonSerialize import JsonSerialize
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.StoreObjects.AccessState import AccessState
from ProjectCode.Domain.MarketObjects.StoreObjects.FounderState import FounderState
from ProjectCode.Domain.MarketObjects.StoreObjects.ManagerState import ManagerState
from ProjectCode.Domain.MarketObjects.StoreObjects.OwnerState import OwnerState


class Access:

    def __init__(self, store, user, nominated_by_username):
        from ProjectCode.Domain.Repository.AccessRepository import AccessRepository
        # self.nominated_by_username = nominated_by_username
        # self.nominations = TypedDict(str, Access) #username, Access
        # self.user = user
        # self.store = store
        # self.access_state = AccessState()
        # self.role = ""
        self.nominated_by_username = nominated_by_username
        self.nominations = []
        self.user = user
        self.store = store
        self.access_state = AccessState()
        self.role = ""

    def __str__(self):
        return self.user.get_username() + " " + self.store.get_store_name() + " " + self.role + " " + self.nominated_by_username

    def setAccess(self, role):
        if role == "Owner":
            self.setOwner()
            self.role = "Owner"
        elif role == "Manager":
            self.setManager()
            self.role = "Manager"
        elif role == "Founder":
            self.setFounder()
            self.role = "Founder"
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
        return False


    def addNominatedUsername(self, username, access):
        self.nominations.append(username)



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


    # def removeAccessFromMember(self):
    #     self.user.get_accesses().pop(self.store.get_store_name())

    def get_user(self):
        return self.user

    def get_store(self):
        return self.store

    def get_role(self):
        return self.role

    def get_access_state(self):
        return self.access_state

    def get_nominated_by_username(self):
        return self.nominated_by_username

    def get_nominations(self):
        if '' in self.nominations:
            return self.nominations[1:]
        return self.nominations

    def get_access_state_name(self):
        return type(self.access_state).__name__[:-5]

    def set_nominations(self, nominations):
        self.nominations = nominations

    # =======================JSON=======================#
    def toJson(self):
        return {
            "user": self.user.toJson(),
            "store": self.store.toJsonInfo(),
            "nominated_by_username": self.nominated_by_username,
            # "nominations": JsonSerialize.toJsonAttributes(self.nominations),
            "role": self.role
            # "access_state": self.access_state.toJson()
        }

