from abc import ABC

from ProjectCode.Domain.Helpers.TypedDict import TypedDict


class AccessState(ABC):



    def __init__(self):
        self.permissions = dict()
        self.permission_names = {"ProductChange": self.addProductPermit, "Bid":self.addBidPermit,
                                 "ModifyPermissions": self.addModifyPermissionPermit, "Auction": self.addAuctionPermit,
                                 "Lottery": self.addLotteryPermit, "StatusChange": self.addChangeStatusPermit, "StaffInfo": self.addStaffViewPermit(),
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


    def addPermission(self,name ,func):
        self.permissions[name] = func

    def checkForPermission(self, name):
        if self.permissions.get(name) is not None:
            return self.permissions[name]()
        else:
            raise Exception("You dont have the permission for that")
