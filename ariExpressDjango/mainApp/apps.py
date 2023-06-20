import sys
from django.apps import AppConfig
import json
from ProjectCode.Service.Service import Service

class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainApp'
    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        load_file = "../load.json"
        config = "../default_config.json"
        # load_file = "../load_purchaseCart.json"
        # load_file = "../load_withDiscounts.json"
        load_file = "../load_withDiscountsAndPolicy.json"
        # load_file = "../load_bids.json"
        # load_file = "../load_registration.json"
        # load_file = "../load_multipleStaff.json"
        
        
        from .views import send_notification_lambda
        service = Service(load_file, config, send_notification_call= send_notification_lambda)
        members = service.getAllMembers()
        # print(f"members status: {members.getStatus()}")
        # print(f"members type: {type(members.getReturnValue())}")
        # print(f"members: {members.getReturnValue()}")
        # print(f"members loads: {json.loads(members.getReturnValue())}")
        # print(f"members loads: {type(json.loads(members.getReturnValue()))}")
        self.loadUsers(json.loads(members.getReturnValue()))
        self.loadAdmins(config)

        # service = Service()

        # service.register("aaa", "asdf1233", "a@a.com") # for debug only
        # service.register("bbb", "asdf1233", "a@a.com") # for debug only
        # service.register("rubin_krief", "h9reynWq", "roobink@post.bgu.ac.il") # for debug only
        # service.register("roobink", "h9reynWq", "roobink@post.bgu.ac.il") # for debug only
        # service.register("Yoav", "XG5EsQtQ.J:k82G", "yoavital98@gmail.com") # for debug only
        # service.logOut("roobink")
        # service.logIn("bbb", "asdf1233")
        # service.createStore("bbb", "TESTSTORE")
        # service.logOut("bbb")


#         load_file = "../load_multipleStaff.json"
# #         load_file = "../load_purchaseCart.json"
#         service = Service(load_file)






        # service.register("aaa", "asdf1233", "a@a.com") # for debug only
        # service.register("bbb", "asdf1233", "a@a.com") # for debug only
        # service.register("rubin_krief", "h9reynWq", "roobink@post.bgu.ac.il") # for debug only
        # service.register("Yoav", "XG5EsQtQ.J:k82G", "yoavital98@gmail.com") # for debug only

        # service.logIn("bbb", "asdf1233")
        # service.createStore("bbb", "TESTSTORE")
        # service.logOut("bbb")

        # service.logIn("aaa", "asdf1233")
        # service.createStore("aaa", "store123")
        # service.createStore("aaa", "456store")
        # service.addNewProductToStore("aaa", "store123", "apple", "fruit", "20", "3")
        # service.addNewProductToStore("aaa", "store123", "banana", "fruit", "30", "8")
        # service.addNewProductToStore("aaa", "store123", "headphones", "electronics", "10", "700")
        # # service.logOut("aaa")
        # # service.logOut("Yoav")
        # #service.logIn("bbb", "asdf1233")
        # rules = {
        #         'rule_type': 'Rule Type',
        #         'product_id': '0',
        #         'operator': '==',
        #         'quantity': '5',
        #         'category': 'asd',
        #         'child': {
        #             'logic_type': 'XOR',
        #             'rule': {
        #                 'rule_type': 'Rule Type',
        #                 'product_id': '0',
        #                 'operator': '>=',
        #                 'quantity': '5',
        #                 'category': 'asd',
        #                 'child':
        #                     {
        #                     'logic_type': 'XOR',
        #                     'rule': {
        #                         'rule_type': 'Rule Type',
        #                         'product_id': '0',
        #                         'operator': '<=',
        #                         'quantity': '5',
        #                         'category': 'asd',
        #                         'child': {}
        #                     }
        #                 }
        #             }
        #         }
        #     }
        
        # service.logIn("bbb", "asdf1233")

        # print(service.addDiscount("store123", "aaa", "Simple", 50, "Product", "1", {}, {}).getStatus())
        # print(service.addDiscount("store123", "aaa", "Conditioned", 20, "Category", "fruit", rules, {}).getStatus())
        # print(service.nominateStoreManager("aaa", "bbb", "store123").getStatus())
        # service.logOut("aaa")

        # TODO: remove the comments
        # service.addNewProductToStore("aaa", "456store", "banana", "fruit", "40", "5")
        # service.addNewProductToStore("aaa", "456store", "banana flavoured lipgloss", "makeup, lipgloss", "20", "25")
        # service.addNewProductToStore("aaa", "456store", "bananas stickers", "craft, art", "10", "5")
        # service.logOut("aaa")
        # service.logIn("rubin_krief", "h9reynWq").getStatus()
        # service.addToBasket("rubin_krief", "store123", 2, 5)
        # service.addToBasket("rubin_krief", "store123", 1, 3)
        # service.addToBasket("rubin_krief", "456store", 1, 2)
        # service.logOut("rubin_krief")

        
        # from django.contrib.auth.models import User
        # users = User.objects.all()
        # for i in range(1, len(users)):
        #     User.objects.all()[i].delete()
    def loadAdmins(self, config):
        from django.contrib.auth.models import User
        with open(config, 'r') as f:
            config_data : dict = json.load(f)
        admins : dict = config_data["Admins"]
        # print(admins)
        # print(type(admins))
        for name, pwd in admins.items():
            # print(name, pwd)
            if not User.objects.filter(username=name).exists():
                user = User.objects.create_user(username=name, password=pwd)
                user.save()

    def loadUsers(self, memberlist):
        from django.contrib.auth.models import User
        for memberDict in memberlist:
            if not User.objects.filter(username=memberDict["username"]).exists():
                user = User.objects.create_user(username=memberDict["username"], password=memberDict["password"], email=memberDict["email"])
                user.save()




