from abc import ABC
import json
from ProjectCode.Domain.Helpers.TypedDict import TypedDict


class AccessState(ABC):



    def __init__(self):
        self.permissions = dict()
        self.permission_names = {"ProductChange": self.addProductPermit, "Bid":self.addBidPermit,
                                 "ModifyPermissions": self.addModifyPermissionPermit, "Auction": self.addAuctionPermit,
                                 "Lottery": self.addLotteryPermit, "StatusChange": self.addChangeStatusPermit, "StaffInfo": self.addStaffViewPermit,
                                 "Policies":  self.addPolicy, "Discounts": self.addDiscount}


    def addPolicy(self):
        return True

    def addDiscount(self):
        return True

    def addProductPermit(self):
        return True

    def addBidPermit(self):
        return True

    def addModifyPermissionPermit(self):
        return True

    def addAuctionPermit(self):
        return True

    def addLotteryPermit(self):
        return True

    def addChangeStatusPermit(self):
        return True


    def addStaffViewPermit(self):
        return True

    def removePermission(self, name):
        if self.permissions.get(name) is None:
            raise Exception("No such permission exists")
        del self.permissions[name]

    def addPermission(self,name ,func=None):
        if func is None:
            self.permissions[name] = self.permission_names[name]
        else:
            self.permissions[name] = func

    #permission is a list of string permissions
    def setPermissions(self, permissions):
        for permission in permissions:
            self.addPermission(permission)


    def get_permissions(self):
        return self.permissions
    
    def get_permissionsAsJson(self):
        return self.toJson()
    
    def checkForPermission(self, name):
        if self.permissions.get(name) is not None:
            return self.permissions[name]
        else:
            raise Exception("You dont have the permission for that")

    # =======================JSON=======================#
    def toJson(self):
        retPermissions = self.permissions
        for key in retPermissions:
                retPermissions[key] = "True"

        # for key in self.permission_names:
        #     if key not in retPermissions:
        #         retPermissions[key] = "False"
        return json.dumps(retPermissions)