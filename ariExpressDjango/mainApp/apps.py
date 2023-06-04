from django.apps import AppConfig
from ProjectCode.Service.Service import Service






class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainApp'
    def ready(self):
        service = Service()
        service.register("aaa", "asdf1233", "a@a.com") # for debug only
        service.register("bbb", "asdf1233", "a@a.com") # for debug only
        service.register("rubin_krief", "h9reynWq", "roobink@post.bgu.ac.il") # for debug only
        service.register("Yoav", "XG5EsQtQ.J:k82G", "yoavital98@gmail.com") # for debug only

        service.logIn("bbb", "asdf1233")
        service.createStore("bbb", "TESTSTORE")
        service.logOut("bbb")

        service.logIn("aaa", "asdf1233")
        service.createStore("aaa", "store123")
        service.createStore("aaa", "456store")
        service.addNewProductToStore("aaa", "store123", "apple", "fruit", "20", "3")
        service.addNewProductToStore("aaa", "store123", "banana", "fruit", "30", "8")
        service.addNewProductToStore("aaa", "store123", "headphones", "electronics", "10", "700")
        # service.logOut("aaa")
        # service.logOut("Yoav")
        #service.logIn("bbb", "asdf1233")
        rules = {
                'rule_type': 'Rule Type',
                'product_id': '0',
                'operator': '==',
                'quantity': '5',
                'category': 'asd',
                'child': {
                    'logic_type': 'XOR',
                    'rule': {
                        'rule_type': 'Rule Type',
                        'product_id': '0',
                        'operator': '>=',
                        'quantity': '5',
                        'category': 'asd',
                        'child':
                            {
                            'logic_type': 'XOR',
                            'rule': {
                                'rule_type': 'Rule Type',
                                'product_id': '0',
                                'operator': '<=',
                                'quantity': '5',
                                'category': 'asd',
                                'child': {}
                            }
                        }
                    }
                }
            }
        
        print(service.addDiscount("store123", "aaa", "Simple", 50, "Product", "1", {}, {}).getStatus())
        print(service.addDiscount("store123", "aaa", "Conditioned", 20, "Category", "fruit", rules, {}).getStatus())
        print(service.nominateStoreManager("aaa", "bbb", "store123").getStatus())
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

        
        # from django.contrib.auth.models import User
        # users = User.objects.all()
        # for i in range(1, len(users)):
        #     User.objects.all()[i].delete()
