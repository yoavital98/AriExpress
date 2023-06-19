from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login as loginFunc
from django.contrib.auth import logout as logoutFunc, authenticate
from django.contrib.auth.forms import UserCreationForm
import os
import sys
from ProjectCode.Service.Service import Service
from .models import *
from .forms import *
from ProjectCode.Service.Response import *
from django.contrib.auth.models import User
from django.contrib import messages
import json
import ast
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect  # for redirecting to another page and clearing the input fields
from django.contrib import messages  # for displaying messages
from django.core.paginator import Paginator  # for pagination
from datetime import datetime  # used to get total msg per day
from django.views.decorators.cache import cache_control  # for disabling cache
from django.utils import timezone

# -------------------------------------------------Notify--------------------------------------------------------------#
from notifications.signals import notify


def sendNotification(reciever_id, notification_id, type, subject):
    receipent = User.objects.get(username=reciever_id)
    sender = User.objects.get(username='ariExpress')
    if receipent.is_authenticated:
        notify.send(sender=sender, recipient=receipent, verb=f'you got a notification from AriExpress!',
                    message_id=notification_id, type=type, description=subject)
    else:
        notification = Notification.objects.create(sender=sender, recipient=receipent, verb=f'you got a notification from AriExpress!',
                                    message_id=notification_id, type=type, description=subject)
        notification.save()



send_notification_lambda = lambda self, receiver_id, notification_id, type, subject: sendNotification(receiver_id,
                                                                                                notification_id,
                                                                                                type, subject)


# ---------------------------------------------------------------------------------------------------------------------#

def startpage(request):
    #Service(send_notification_call=send_notification_lambda)
    return render(request, "startpage.html")


def mainpage(request):
    # ------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------
    # --------------------------TODO: DELETE THESE LINES----------------------------
    # from django.contrib.auth.models import User
    # Service().logInFromGuestToMember(0, "aaa", "asdf1233")
    # user = authenticate(request, username='aaa', password='asdf1233')
    # loginFunc(request, user)
    # request.session['guest'] = 0
    # ------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------

    # ----------------------creating first user - ariExpress--------------------------------------------
    if not User.objects.filter(username='ariExpress').exists():
        user = User.objects.create_user(username='ariExpress', password='ariExpress')
        user.save()
    # --------------------------------------------------------------------------------------------------
    createGuestIfNeeded(request)
    return render(request, 'mainpage.html')


def login(request):
    msg = ""
    # login form is sent
    if request.method == 'POST':
        if request.user.is_authenticated and not request.session['guest']:  # user (not guest) is logged in
            messages.success(request, ("Error: A User is already logged in"))
            return render(request, 'login.html', {'form': loginForm()})
        elif request.user.is_authenticated and request.session['guest']:  # user (guest) is logged in
            # service = Service()

            form = loginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                if Service().checkIfAdmin(username).getStatus():
                    actionRes = Service().logIn(username, password)
                    if actionRes.getStatus():
                        user = authenticate(request, username=username, password=password)
                        loginFunc(request, user)
                        request.session['guest'] = 0
                        messages.success(request, (f"{username} Logged in successfully"))
                        return redirect('mainApp:mainpage')
                    else:
                        # Service().logOut # TODO: needed?
                        request.session['guest'] = 1
                        messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
                        return redirect('mainApp:login')
                else:
                    check = guestToUser(request, username, password)
                    if check:
                        request.session['guest'] = 0
                        messages.success(request, (f"{check} Logged in successfully"))
                        return redirect('mainApp:mainpage')
                    else:
                        request.session['guest'] = 1
                        messages.success(request, (f"Error: A User is already logged in (shouldn't get here) - MAYBE THE USER NOT IN THE DJANGO DB?"))
                        return redirect('mainApp:login')

                # if request.session['guest']:
                #     res = service.logIn(username, password)
                #     if res.getStatus() == True:
                #         if not request.session['guest']:                                        # regular login
                #             user = authenticate(request, username=username, password=password)
                #             loginFunc(request, user)
                #             request.session['guest'] = 0
                #             messages.success(request, (f"{username} Logged in successfully"))
                #             return redirect('mainApp:mainpage')
                #         else:                                                                   # guest to member login
                #             loggedin_username = guestToUser(request, username, password)
                #             if loggedin_username: return loggedin_username
                #             else: return False                                                  # shouldn't happen

                # else:
                #     guestToUser(request, username, password)
                #     return redirect('mainApp:mainpage')
            else:
                messages.success(request, ("Error: login form is not valid"))
        else:
            messages.success(request, ("Error: something went wrong with the login"))

    # render the login page
    form = loginForm()
    return render(request, 'login.html', {'form': form})


def registerPage(request):
    if request.method == 'POST':
        service = Service()
        if request.user.is_authenticated and not request.session['guest']:  # user (not guest) is logged in

            messages.success(request, ("Error: A User is already logged in"))
            return render(request, 'login.html', {'form': loginForm()})
        elif request.user.is_authenticated and request.session['guest']:  # user (guest) is logged in
            form = CreateMemberForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                email = form.cleaned_data['email']
                res = service.register(username, password, email)
                if res.getStatus():
                    form.save()
                    # user = authenticate(request, username=username, password=password)
                    # loginFunc(request, user)
                    request.session['guest'] = 1
                    check = guestToUser(request, username, password)
                    if check:
                        request.session['guest'] = 0
                        messages.success(request, (f"{username} Registered successfully"))
                        return redirect('mainApp:mainpage')
                    else:
                        User.objects.filter(username=username).delete()  # remove the created user from django
                        messages.success(request, (f"Error: register was successful but there is a login error"))
                else:
                    messages.success(request, (f"Error: {res.getReturnValue()}"))
            else:
                messages.success(request, ("Error: register form is not valid"))
        else:
            messages.success(request, ("Error: something went wrong with the register"))

    # render the register page
    form = CreateMemberForm()
    return render(request, 'register.html', {'form': form})


def logout(request):
    # if request.user.is_authenticated and not request.user.username.startswith("GuestUser"):
    if request.user.is_authenticated and not request.session['guest']:
        service = Service()
        actionRes = service.logOut(request.user.username)
        if actionRes.getStatus():
            logoutFunc(request)
            request.session['guest'] = 1
            return redirect('mainApp:mainpage')
        else:
            messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
            return redirect('mainApp:mainpage')
    elif request.session["guest"]:
        messages.success(request, ("Error: cannot logout as guest"))
        return redirect('mainApp:mainpage')
    else:
        messages.success(request, ("Error: need to be logged in first"))
        return redirect('mainApp:mainpage')


def mystores(request):
    if request.user.is_authenticated:
        service = Service()
        storesInfo = service.getUserStores(request.user.username)
        string_data = storesInfo.getReturnValue()
        storesInfoDict = ast.literal_eval(str(string_data))
        return render(request, 'mystores.html', {'stores': storesInfoDict})
    messages.success(request, ("Error: User is not logged in (django error)"))
    return redirect('mainApp:mainpage')


def viewStoreStaff(request, storename):
    username = request.user.username
    service = Service()
    if 'removeAccessButton' in request.POST:
        requester_id = username
        to_remove_id = request.POST.get('to_remove_id')
        actionRes = service.removeAccess(requester_id, to_remove_id, storename)
        if actionRes.getStatus():
            messages.success(request, (f"{requester_id} has removed {to_remove_id} accesses"))
            return redirect('mainApp:viewStoreStaff', storename=storename)
        else:
            messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
            return redirect('mainApp:viewStoreStaff', storename=storename)
    else:  # just render page
        permissionName = 'StaffInfo'
        if permissionCheck(username, storename, permissionName):
            actionRes = service.getStoreProductsInfo(storename)
            if actionRes.getStatus():
                staff = actionRes.getReturnValue()['accesses']
                staff = ast.literal_eval(str(staff))
            return render(request, 'viewStoreStaff.html', {'storename': storename, 'staff': staff})
        else:
            messages.success(request, (f"Error: {username} doesn't have {permissionName} permission"))
            return redirect('mainApp:store_specific', storename=storename)

    messages.success(request, (f"Error: Something went wrong"))
    return redirect('mainApp:store_specific', storename=storename)


def viewAllStores(request):
    service = Service()
    storesInfo = service.getStoresBasicInfo()
    string_data = storesInfo.getReturnValue()
    storesInfoDict = ast.literal_eval(str(string_data))
    return render(request, 'allStores.html', {'stores': storesInfoDict})


def store_specific(request, storename):
    service = Service()
    username = request.user.username
    if request.user.is_authenticated:
        permissions = service.getPermissionsAsJson(storename, username).getReturnValue()
        permissions = ast.literal_eval(str(permissions))
    else:
        permissions = {}

    # print(permissions)
    # print(storename)
    # print(username)

    if 'openStore' in request.POST:
        permissionName = 'StatusChange'
        if permissionCheck(username, storename, permissionName):
            actionRes = service.openStore(request.user.username, storename)
            if actionRes.getStatus():
                messages.success(request, ("Store is now open."))
                return redirect('mainApp:store_specific', storename=storename)
            else:
                messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
                return redirect('mainApp:mystores')
        else:
            messages.success(request, (f"Error: {username} doesn't have {permissionName} permission"))
            return redirect('mainApp:store_specific', storename=storename)

    if 'closeStore' in request.POST:
        permissionName = 'StatusChange'
        if permissionCheck(username, storename, permissionName):
            actionRes = service.closeStore(request.user.username, storename)
            if actionRes.getStatus():
                messages.success(request, ("Store is now closed."))
                return redirect('mainApp:store_specific', storename=storename)
            else:
                messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
                return redirect('mainApp:mystores')
        else:
            messages.success(request, (f"Error: {username} doesn't have {permissionName} permission"))
            return redirect('mainApp:store_specific', storename=storename)

    if 'removeProduct' in request.POST:
        permissionName = 'ProductChange'
        if permissionCheck(username, storename, permissionName):
            product_id = request.POST.get('product_id')
            actionRes = service.removeProductFromStore(request.user.username, storename, product_id)
            if actionRes.getStatus():
                messages.success(request, ("Product has been removed"))
                return redirect('mainApp:store_specific', storename=storename)
            else:
                messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
                return redirect('mainApp:mystores')
        else:
            messages.success(request, (f"Error: {username} doesn't have {permissionName} permission"))
            return redirect('mainApp:store_specific', storename=storename)

    else:
        products = service.getStoreProductsInfo(storename).getReturnValue()
        # context = request.POST.get('data')
        context = ast.literal_eval(str(products))
        products_dict = json.loads(context['products'])  # Parse JSON string into a dictionary
        #products_dict = ast.literal_eval(str(products_dict))
        products_list = []
        for product in products_dict.values():
            products_list.append(product)
        active = "Open" if context['active'].lower() == "true" else "Closed"
        return render(request, 'store_specific.html',
                      {'products': products_list, 'storename': storename, 'active': active, 'permissions': permissions})
    # else:
    #     return redirect('mainApp:mainpage')


# def openStore(request, storename):
#     if request.method == 'POST' and request.user.is_authenticated:
#         service = Service(sendNotification)
#         actionRes = service.openStore(request.user.username, storename)
#         if actionRes.getStatus():
#             messages.success(request, ("Store is now open."))
#             return redirect('mainApp:store_specific', storename=storename)
#         else:
#             messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
#             return redirect('mainApp:mystores')
#     return redirect('mainApp:mainpage')


# def closeStore(request, storename):
#     if request.method == 'POST' and request.user.is_authenticated:
#         service = Service(sendNotification)
#         actionRes = service.closeStore(request.user.username, storename)
#         if actionRes.getStatus():
#             messages.success(request, ("Store is now closed."))
#             return redirect('mainApp:store_specific', storename=storename)
#         else:
#             messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
#             return redirect('mainApp:mystores')
#     return redirect('mainApp:mainpage')

def editProduct(request, storename):
    permissionName = 'ProductChange'
    username = request.user.username
    if permissionCheck(username, storename, permissionName):
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        product_quantity = request.POST.get('product_quantity')
        product_price = request.POST.get('product_price')
        product_categories = request.POST.get('product_categories')

        if 'editButton' in request.POST:
            service = Service()
            actionRes = service.editProductOfStore(request.user.username, storename, product_id, name=product_name,
                                                   quantity=product_quantity, price=product_price,
                                                   categories=product_categories)
            if actionRes.getStatus():
                messages.success(request, ("Product has been edited"))
                return redirect('mainApp:store_specific', storename=storename)

        return render(request, 'editProduct.html', {'storename': storename,
                                                    'product_name': product_name,
                                                    'product_quantity': product_quantity,
                                                    'product_price': product_price,
                                                    'product_categories': product_categories})
    else:
        messages.success(request, (f"Error: {username} doesn't have {permissionName} permission"))
        return redirect('mainApp:store_specific', storename=storename)


def addNewDiscount(request, storename):  # Discounts
    username = request.user.username
    permissionName = 'Discounts'
    if permissionCheck(username, storename, permissionName):
        discountTypeInt = None if request.POST.get('discountType') == None else int(request.POST.get('discountType'))
        discountType = None if discountTypeInt == None else getDiscountType(discountTypeInt)
        percent = 50 if request.POST.get('discountAmountRange') == None else int(
            request.POST.get('discountAmountRange'))
        levelTypeInt = None if request.POST.get('levelType') == None else int(request.POST.get('levelType'))
        levelType = None if levelTypeInt == None else getDiscountLevelType(levelTypeInt)
        levelName = "" if request.POST.get('levelName') == None else request.POST.get('levelName')

        if 'submitDiscount' in request.POST:
            service = Service()
            if discountTypeInt == 1:
                actionRes = service.addDiscount(storename, username, discountType, percent, levelType, levelName)
                if actionRes.getStatus():
                    messages.success(request, ("Discount has been added"))
                else:
                    messages.success(request, (f"Error: {actionRes.getReturnValue()}"))

            if discountTypeInt == 2:
                discountRulesData = request.session['discountRulesData']
                fixedRulesData = fixDiscountRulesData(discountRulesData)
                actionRes = service.addDiscount(storename, username, discountType, percent, levelType, levelName,
                                                fixedRulesData)
                if actionRes.getStatus():
                    messages.success(request, ("Discount has been added"))
                    if 'discountRulesData' in request.session:
                        del request.session['discountRulesData']
                else:
                    messages.success(request, (f"Error: {actionRes.getReturnValue()}"))

            if discountTypeInt == 3:
                pass

            if discountTypeInt == 4:
                return addNewDiscountSpecial(request, storename, "Max")

            if discountTypeInt == 5:
                return addNewDiscountSpecial(request, storename, "Add")


        if 'conditionedAddRule' in request.POST:
            # Retrieve the submitted discountRulesData
            discountRulesData = request.POST.get('discountRulesData')
            ruleData = json.loads(discountRulesData)

            if 'discountRulesData' not in request.session:
                request.session['discountRulesData'] = {}
                request.session['discountRuleCounter'] = 0

            # Check if ruleData is not already in the session
            if ruleData not in dict(request.session['discountRulesData']).values():
                counter = request.session['discountRuleCounter']
                ruleDict = request.session['discountRulesData']
                ruleDict[counter] = ruleData
                request.session['discountRuleCounter'] += 1

        if 'clearAllRules' in request.POST:
            if 'discountRulesData' in request.session:
                del request.session['discountRulesData']
            request.session['discountRuleCounter'] = 0

        return render(request, 'addNewDiscount.html',
                      {'storename': storename, 'percent': percent, 'discountType': discountType, 'levelType': levelType,
                       'levelName': levelName})
    else:
        messages.success(request, (f"Error: {username} doesn't have {permissionName} permission"))
        return redirect('mainApp:store_specific', storename=storename)


def addNewDiscountSpecial(request, storename, discount_type):
    username = request.user.username
    permissionName = 'Discounts'
    if permissionCheck(username, storename, permissionName):
        service = Service()
        discountTypeInt = None if request.POST.get('discountType') == None else int(request.POST.get('discountType'))
        discountType = None if discountTypeInt == None else getDiscountType(discountTypeInt)
        percent = 50 if request.POST.get('discountAmountRange') == None else int(
            request.POST.get('discountAmountRange'))
        levelTypeInt = None if request.POST.get('levelType') == None else int(request.POST.get('levelType'))
        levelType = None if levelTypeInt == None else getDiscountLevelType(levelTypeInt)
        levelName = "" if request.POST.get('levelName') == None else request.POST.get('levelName')

        if 'addDiscount' in request.POST:
            if discountTypeInt == 1:
                newdiscount = {"discount_type": "Simple", "percent": percent, "level": levelType, "level_name": levelName}
                if 'discountsData' not in request.session:
                    request.session['discountsData'] = {}
                    request.session['discountCounterSpecial'] = 1
                counter = request.session['discountCounterSpecial']
                request.session['discountsData'][counter] = newdiscount
                request.session['discountCounterSpecial'] = int(request.session['discountCounterSpecial']) + 1
                print(f"discounts: {request.session['discountsData']}")
                print(f"counter: {request.session['discountCounterSpecial']}")
                messages.success(request, (f"Discount has been added to the \"{discount_type}\" list"))

            if discountTypeInt == 2:
                discountRulesData = request.session['discountRulesDataSpecial']
                fixedRulesData = fixDiscountRulesData(discountRulesData)
                newdiscount = {"discount_type": "Conditioned", "percent": percent, "level": levelType, "level_name": levelName, "rule": fixedRulesData}
                if 'discountsData' not in request.session:
                    request.session['discountsData'] = {}
                    request.session['discountCounterSpecial'] = 1
                counter = request.session['discountCounterSpecial']
                request.session['discountsData'][counter] = newdiscount
                request.session['discountCounterSpecial'] = int(request.session['discountCounterSpecial']) + 1
                print(f"discounts: {request.session['discountsData']}")
                print(f"counter: {request.session['discountCounterSpecial']}")
                messages.success(request, (f"Discount has been added to the \"{discount_type}\" list"))

            # if discountTypeInt == 3:
            #     pass

            # if discountTypeInt == 4:
            #     return addNewDiscountSpecial(request, storename, "Max")

            # if discountTypeInt == 5:
            #     return addNewDiscountSpecial(request, storename, "Add")


        if 'conditionedAddRule' in request.POST:
            # Retrieve the submitted discountRulesDataSpecial
            discountRulesDataSpecial = request.POST.get('discountRulesDataSpecial')
            ruleData = json.loads(discountRulesDataSpecial)

            if 'discountRulesDataSpecial' not in request.session:
                request.session['discountRulesDataSpecial'] = {}
                request.session['discountRuleCounterSpecial'] = 0

            # Check if ruleData is not already in the session
            if ruleData not in dict(request.session['discountRulesDataSpecial']).values():
                counter = request.session['discountRuleCounterSpecial']
                ruleDict = request.session['discountRulesDataSpecial']
                ruleDict[counter] = ruleData
                request.session['discountRuleCounterSpecial'] += 1

        if 'clearAllRules' in request.POST:
            if 'discountRulesDataSpecial' in request.session:
                del request.session['discountRulesDataSpecial']
            request.session['discountRuleCounterSpecial'] = 0

        if 'sendDiscount' in request.POST:
            discounts = request.session['discountsData']
            discounts = fixDiscountSpecial(discounts)
            print(f"final dict: {discounts}")
            print(f"type: {discount_type}")
            actionRes = service.addDiscount(storename, username, discount_type, discounts=discounts)
            if actionRes.getStatus():
                messages.success(request, ("Discount has been added"))
                if 'discountRulesDataSpecial' in request.session:
                    del request.session['discountRulesDataSpecial']
                if 'discountsData' in request.session:
                    del request.session['discountsData']
                if 'discountRuleCounterSpecial' in request.session:
                    del request.session['discountRuleCounterSpecial']
                if 'discountCounterSpecial' in request.session:
                    del request.session['discountCounterSpecial']
                return redirect('mainApp:store_specific', storename=storename)
            else:
                messages.success(request, (f"Error: {actionRes.getReturnValue()}"))

        if 'resetInfo' in request.POST:
            if 'discountRulesDataSpecial' in request.session:
                del request.session['discountRulesDataSpecial']
            if 'discountsData' in request.session:
                del request.session['discountsData']
            if 'discountRuleCounterSpecial' in request.session:
                del request.session['discountRuleCounterSpecial']
            if 'discountCounterSpecial' in request.session:
                del request.session['discountCounterSpecial']
                

        # init discounts data

        if 'discountsData' not in request.session:
            request.session['discountsData'] = {}
            request.session['discountRuleCounterSpecial'] = 0
            request.session['discountCounterSpecial'] = 1
            request.session['discountRulesDataSpecial'] = {}
            
        return render(request, 'addNewDiscountSpecial.html', {'storename': storename, 'discount_type': discount_type})

    else:
        messages.success(request, (f"Error: {username} doesn't have {permissionName} permission"))
        return redirect('mainApp:store_specific', storename=storename)




def addNewPurchasePolicy(request, storename):  # Policies
    username = request.user.username
    permissionName = 'Policies'
    if permissionCheck(username, storename, permissionName):
        purchase_policy_int = None if request.POST.get('purchase_policy') == None else int(
            request.POST.get('purchase_policy'))
        purchase_policy = None if purchase_policy_int == None else getPurchasePolicyType(purchase_policy_int)
        levelTypeInt = None if request.POST.get('levelType') == None else int(request.POST.get('levelType'))
        levelType = None if levelTypeInt == None else getPolicyLevelType(levelTypeInt)
        levelName = None if request.POST.get('levelName') == None else request.POST.get('levelName')

        if 'submitPolicy' in request.POST:
            service = Service()
            if purchase_policy_int == 1:
                policyRulesData = request.session['policyRulesData']
                # print(f"policyRulesData: {policyRulesData}")
                rule = fixDiscountRulesData(policyRulesData)  # TODO: check if works
                # print(f"storename: {storename}\n username: {username}\n, purchase_policy: {purchase_policy}\n, rule: {rule}\n, levelType: {levelType}\n, levelName: {levelName}")
                actionRes = service.addPurchasePolicy(storename, username, purchase_policy, rule, levelType, levelName)
                if actionRes.getStatus():
                    messages.success(request, ("Policy has been added"))
                else:
                    messages.success(request, (f"Error: {actionRes.getReturnValue()}"))

            if purchase_policy_int == 2:
                pass

            if purchase_policy_int == 3:
                pass

            if purchase_policy_int == 4:
                pass

            if purchase_policy_int == 5:
                pass

        if 'addRule' in request.POST:
            # Retrieve the submitted policyRulesData
            policyRulesData = request.POST.get('policyRulesData')
            ruleData = json.loads(policyRulesData)

            if 'policyRulesData' not in request.session:
                request.session['policyRulesData'] = {}
                request.session['policyRuleCounter'] = 0

            # Check if ruleData is not already in the session
            if ruleData not in dict(request.session['policyRulesData']).values():
                counter = request.session['policyRuleCounter']
                ruleDict = request.session['policyRulesData']
                ruleDict[counter] = ruleData
                request.session['policyRuleCounter'] += 1

        if 'clearAllRules' in request.POST:
            if 'policyRulesData' in request.session:
                del request.session['policyRulesData']
            request.session['policyRuleCounter'] = 0

        return render(request, 'addNewPurchasePolicy.html', {'storename': storename})

    else:
        messages.success(request, (f"Error: {username} doesn't have {permissionName} permission"))
        return redirect('mainApp:store_specific', storename=storename)

def viewBids(request, storename):
    permissionName = 'Bid'
    username = request.user.username
    if permissionCheck(username, storename, permissionName):
        service = Service()
        if 'approveBid' in request.POST:
            bid_id = int(request.POST.get('bid_id'))
            actionRes = service.approveBid(request.user.username, storename, bid_id)
            if not actionRes.getStatus():
                messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
                return redirect('mainApp:viewBids', storename=storename)
            else:
                messages.success(request, (f"Bid {bid_id} was approved"))

        if 'rejectBid' in request.POST:
            bid_id = int(request.POST.get('bid_id'))
            actionRes = service.rejectBid(request.user.username, storename, bid_id)
            if not actionRes.getStatus():
                messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
                return redirect('mainApp:viewBids', storename=storename)
            else:
                messages.success(request, (f"Bid {bid_id} was rejected"))

        if 'offerBidPrice' in request.POST:
            bid_id = int(request.POST.get('bid_id'))
            offerNumber = int(request.POST.get('offerNumber'))
            actionRes = service.sendAlternativeOffer(request.user.username, storename, bid_id, offerNumber)
            if not actionRes.getStatus():
                messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
                return redirect('mainApp:viewBids', storename=storename)
            else:
                messages.success(request, (f"Offer for bid {bid_id} sent successfully"))

        bids = {}
        actionRes = service.getAllBidsFromStore(storename)
        if actionRes.getStatus():
            bids : dict = ast.literal_eval(str(actionRes.getReturnValue()))
            for id, bid in bids.items():
                id = int(id)
                staff = service.getStaffPendingForBid(storename, id)
                # print(f"status {staff.getStatus()}")
                # print(f"value {staff.getReturnValue()}")
                # print(f"valuetype {type(staff.getReturnValue())}")
                bid["staffToApprove"] = ast.literal_eval(str(staff.getReturnValue()))
        return render(request, 'viewBids.html', {'storename': storename,
                                                    'bids': bids
                                                    })
    else:
        messages.success(request, (f"Error: {username} doesn't have {permissionName} permission"))
        return redirect('mainApp:store_specific', storename=storename)

def userBids(request):
    username = request.user.username
    service = Service()
    if 'purchaseBid' in request.POST:
        return checkoutpage_bids(request)
        bid_id = int(request.POST.get('bid_id'))
        actionRes = service.purchaseConfirmedBid(request.user.username, storename, bid_id)
        if not actionRes.getStatus():
            messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
            return redirect('mainApp:userBids')
        else:
            messages.success(request, (f"Bid {bid_id} was approved"))

    bids = {}
    actionRes = service.getAllBidsFromUser(username)
    if actionRes.getStatus():
        bids : dict = ast.literal_eval(str(actionRes.getReturnValue()))
    # print(f"final bids: {bids}")
    return render(request, 'userBids.html', {'bids': bids
                                                })

def createStore(request):
    if request.method == 'POST' and request.user.is_authenticated:
        newStoreName = request.POST.get('storeName')
        service = Service()
        res = service.createStore(request.user.username, newStoreName)
        if res.getStatus():
            messages.success(request, ("A new store has been created successfully"))
            return redirect('mainApp:mystores')
        else:
            msg = res.getReturnValue()
            messages.success(request, (f"Error: {msg}"))
            return redirect('mainApp:mainpage')
    else:
        return render(request, 'createStore.html', {})


def nominateUser(request, storename):
    service = Service()
    username = request.user.username
    permissionName = 'ModifyPermissions'

    if permissionCheck(username, storename, permissionName):
        if request.method == 'POST':
            requesterUsername = request.user.username
            toBeNominatedUsername = request.POST.get('inputNominatedUsername')
            selected = request.POST.get('nominateSelect')
            store_name = request.POST.get('storename')
            if selected == '1':
                res = service.nominateStoreOwner(requesterUsername, toBeNominatedUsername, store_name)
                if res.getStatus():
                    messages.success(request, ("A new user has been nominated to be Owner."))
                    return redirect('mainApp:mystores')
                else:
                    messages.success(request, (f"Error: {res.getReturnValue()}"))
                    return redirect('mainApp:mystores')
            elif selected == '2':
                res = service.nominateStoreManager(requesterUsername, toBeNominatedUsername, store_name)
                if res.getStatus():
                    messages.success(request, ("A new user has been nominated to be Manager."))
                    return redirect('mainApp:mystores')
                else:
                    messages.success(request, ("Error nominating a user to be Manager"))
                    return redirect('mainApp:mystores')
            else:
                return render(request, 'nominateUser.html',
                              {'storename': storename})  # didn't nominate yet, just load the page


        else:
            return render(request, 'nominateUser.html', {'storename': storename})

    else:
        messages.success(request, (f"Error: {username} doesn't have {permissionName} permission"))
        return redirect('mainApp:store_specific', storename=storename)

    # return render(request, 'store_specific.html', {'storename': storename})


def addNewProduct(request, storename):
    permissionName = 'ProductChange'
    username = request.user.username
    if permissionCheck(username, storename, permissionName):
        if "openAddNewProduct" in request.POST:
            return render(request, 'addNewProduct.html', {'storename': storename})

        else:
            form = NewProductForm(request.POST)
            if form.is_valid():
                productname = form.cleaned_data['productName']
                category = form.cleaned_data['productCategory']
                price = form.cleaned_data['productPrice']
                quantity = form.cleaned_data['productQuantity']
                service = Service()
                actionRes = service.addNewProductToStore(request.user.username, storename, productname,
                                                         quantity, price, category)

                if actionRes.getStatus():
                    messages.success(request, ("A new Product has been added to the store"))
                    return redirect('mainApp:store_specific', storename=storename)
                else:
                    messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
                    return redirect('mainApp:store_specific', storename=storename)
            else:
                # Handle the case when the form is invalid
                messages.error(request, "Invalid form data")
                return redirect('mainApp:addNewProduct', storename=storename)
    else:
        messages.success(request, (f"Error: {username} doesn't have {permissionName} permission"))
        return redirect('mainApp:store_specific', storename=storename)


def viewDiscounts(request, storename):
    service = Service()
    permissionName = 'Discounts'
    username = request.user.username
    if permissionCheck(username, storename, permissionName):
        actionRes = service.getAllDiscounts(storename)
        if actionRes.getStatus():
            removeNulls = actionRes.getReturnValue().replace("null", "\"\"")
            # print(removeNulls)
            discounts = ast.literal_eval(str(removeNulls))
            return render(request, 'viewDiscounts.html', {'storename': storename, 'discounts': discounts})
        else:
            messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
            return redirect('mainApp:store_specific', storename=storename)
    messages.success(request, (f"Error: {username} doesn't have {permissionName} permission"))
    return redirect('mainApp:store_specific', storename=storename)


def adminPage(request):
    if request.user.is_superuser:
        return render(request, 'adminPage.html', {})
    else:
        messages.success(request, ("Cannot access ADMIN area because you are not an admin."))
        return redirect('mainApp:mainpage')


def viewOnlineUsers(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            service = Service()
            resOnline = service.getAllOnlineMembers(request.user.username)
            resOffline = service.getAllOfflineMembers(request.user.username)
            if resOnline.getStatus() and resOffline.getStatus():
                onlinemembers = resOnline.getReturnValue()  # returns a list
                offlinemembers = resOffline.getReturnValue()  # returns a list
                onlinemembers = ast.literal_eval(str(onlinemembers))
                offlinemembers = ast.literal_eval(str(offlinemembers))
                context = {'online': onlinemembers,
                           'offline': offlinemembers}
                return render(request, 'adminPage.html', {'context': context})

    messages.success(request, ("Cannot access ADMIN area because you are not an admin."))
    return redirect('mainApp:mainpage')


def reset_password(request):
    pass


def homepage_guest(request):
    pass


@login_required(login_url='/login')
def inbox(request):
    if request.user.is_authenticated:
        service = Service()
        all_user_messages = service.getAllMessagesReceived(request.user.username)
        if all_user_messages.getStatus():
            all_user_notifications = service.getAllNotifications(request.user.username)
            if all_user_notifications.getStatus():
                all_user_messages = all_user_messages.getReturnValue()
                all_user_notifications = all_user_notifications.getReturnValue()
                paginator = Paginator(all_user_messages, 5)
                page = request.GET.get('page')
                all_messages = paginator.get_page(page)
                return render(request, 'inbox.html',
                            {'usermessages': all_messages, 'usernotifications': all_user_notifications})
            else:
                messages.error(request, "Error: " + str(all_user_notifications.getReturnValue()))
                return redirect('mainApp:mainpage')
        else:
            messages.error(request, "Error: " + str(all_user_messages.getReturnValue()))
            return redirect('mainApp:mainpage')
    else:
        messages.error(request, "Error: User not authenticated")
        return redirect('mainApp:mainpage')


def send_message(request):
    if request.method == 'POST':
        service = Service()
        form = UserMessageform(request.POST, request.FILES)
        if form.is_valid():
            receiver_username = form.cleaned_data['receiver']
            res = service.checkUsernameExistence(receiver_username)
            if res.getStatus():
                subject = form.cleaned_data['subject']
                content = form.cleaned_data['content']
                creation_date = datetime.now()
                file = form.cleaned_data['file']
                print(file)
                message_res = service.sendMessageUsers(request.user.username, receiver_username, subject, content, creation_date,file)
                if message_res.getStatus():

                    messages.success(request, "Message sent successfully")
                    return HttpResponseRedirect('/inbox')
                else:
                    messages.error(request,
                                   "Error sending message through backend - " + str(message_res.getReturnValue()))
            else:
                messages.error(request, "Invalid adresssee username - the message was not sent")
        else:
            messages.error(request, "Invalid form submission - " + form.errors.as_json())
    else:
        form = UserMessageform()
        messages.error(request, "Error sending message")
    return HttpResponseRedirect('/inbox')


@login_required(login_url='/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_message(request, usermessage_id):
    service = Service()
    res = service.deleteMessage(request.user.username, usermessage_id)
    if res.getStatus():
        notification = Notification.objects.filter(message_id=usermessage_id, recipient=request.user, type='message')
        notification.delete()
        messages.success(request, "Message deleted successfully")
    else:
        messages.success(request, "Error deleting message - " + str(res.getReturnValue()))
    return HttpResponseRedirect('/inbox')


@login_required(login_url='/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mark_as_read(request, usermessage_id):
    service = Service()

    res = service.readMessage(request.user.username, usermessage_id)
    if res.getStatus():
        notification = Notification.objects.filter(message_id=usermessage_id, recipient=request.user, type='message')[0]
        notification.mark_as_read()
        messages.success(request, "Message marked as read successfully")
    else:
        messages.error(request, "Error marking message as read - " + str(res.getReturnValue()))
    return HttpResponseRedirect('/inbox')


@login_required(login_url='/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mark_notification_as_read(request, notification_id):
    service = Service()
    res = service.readNotification(request.user.username, notification_id)
    if res.getStatus():
        notification = Notification.objects.filter(message_id=notification_id, recipient=request.user, type='notification')[0]
        notification.mark_as_read()
        messages.success(request, "Message marked as read successfully")
    else:
        messages.error(request, "Error marking notification as read - " + str(res.getReturnValue()))
    return HttpResponseRedirect('/inbox')

@login_required(login_url='/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_notification(request, notification_id):
    service = Service()
    res = service.deleteNotification(request.user.username, notification_id)
    if res.getStatus():
        notification = Notification.objects.filter(message_id=notification_id, recipient=request.user, type='notification')
        notification.delete()
        messages.success(request, "notification deleted successfully")
    else:
        messages.success(request, "Error deleting notification - " + str(res.getReturnValue()))
    return HttpResponseRedirect('/inbox')

# check if username exists
def check_username(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        service = Service()
        res = service.checkUsernameExistence(username)
        if res.getStatus():
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False})


# ---------------------------------------------------------cart functionality---------------------------------------------------------#
def cart(request):
    if request.user.is_authenticated:
        service = Service()
        res = service.getCart(request.user.username)
        if res.getStatus():
            cart = res.getReturnValue()
            baskets = ast.literal_eval(str(cart)).get('baskets')
            baskets = ast.literal_eval(str(baskets))
            products = dict()
            for basket in baskets:
                basket_res = service.getBasket(request.user.username, basket)
                if basket_res.getStatus() == True:
                    basket_res = basket_res.getReturnValue()
                    basket_products = ast.literal_eval(str(basket_res)).get('products')
                    basket_products = ast.literal_eval(str(basket_products))
                    # for product in basket_products.values():
                    #     product['product'] = json.loads(product['product'])
                    total_price = calculate_total_price(basket_products)
                    products[basket] = {'items': basket_products, 'total_price': total_price}

            return render(request, 'cart.html', {'baskets': baskets, 'products': products})
        else:
            messages.error(request, "Error loading cart - " + str(res.getReturnValue()))
            return redirect('mainApp:mainpage')
    else:
        messages.error(request, "You must be logged in to view your cart")
        return HttpResponseRedirect('/login')


def calculate_total_price(products):
    total_price = 0
    for product in products.values():
        total_price += float(product['price']) * float(product['quantity'])
    return total_price


@login_required(login_url='/login')
def remove_basket_product(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            service = Service()
            form = BasketRemoveProductForm(request.POST)
            if form.is_valid():
                store = form.cleaned_data['store_name']
                product_id = form.cleaned_data['product_id']
                res = service.removeFromBasket(request.user.username, store, product_id)
                if res.getStatus():
                    messages.success(request, "Product removed from cart successfully")
                    return HttpResponseRedirect('/cart')
                else:
                    messages.error(request, "Error removing product from cart - " + str(res.getReturnValue()))
                    return HttpResponseRedirect('/cart')
            else:
                messages.error(request, "Error removing product from cart - " + str(form.errors))
                return HttpResponseRedirect('/cart')
        else:
            messages.error(request, "You must be logged in to view your cart")
            return HttpResponseRedirect('/login')
    else:
        form = BasketRemoveProductForm()
        messages.error(request, "Error removing product from cart - " + str(request.method))
        return HttpResponseRedirect('/cart')


@login_required(login_url='/login')
def edit_basket_product(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            service = Service()
            form = BasketEditProductForm(request.POST)
            if form.is_valid():
                store = form.cleaned_data['store_name']
                product_id = form.cleaned_data['product_id']
                quantity = form.cleaned_data['quantity']
                res = service.editBasketQuantity(request.user.username, store, product_id, quantity)
                if res.getStatus():
                    messages.success(request, "quantity edited successfully")
                    return HttpResponseRedirect('/cart')
                else:
                    messages.error(request, "Error editting product quantity res - " + str(res.getReturnValue()))
                    return HttpResponseRedirect('/cart')
            else:
                messages.error(request, "Error editting product quantity form - " + str(form.errors))
                return HttpResponseRedirect('/cart')
        else:
            messages.error(request, "You must be logged in to view your cart")
            return HttpResponseRedirect('/login')
    else:
        form = BasketEditProductForm()
        messages.error(request, "Error editting product quantity - " + str(request.method))
        return HttpResponseRedirect('/cart')

@login_required(login_url='/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkoutpage_bids(request):
    if request.user.is_authenticated:
        service = Service()
        actionRes = service.getAllBidsFromUser(request.user.username)
        if actionRes.getStatus():
            username = request.user.username
            cart = actionRes.getReturnValue()
            allbids = ast.literal_eval(str(cart))
            bid_id = request.POST.get('bid_id')
            bid = allbids[bid_id]
            # print(f"allbids {allbids}")
            # print(f"allbidstype {type(allbids)}")
            # print(request.POST.get('bid_id'))
            print(f"bid {bid}")
            product = service.getProduct(bid["storename"], bid["product_id"], username).getReturnValue()
            product = ast.literal_eval(str(product))
            print(f"product {product}")
            print(f"product type {type(product)}")
            return render(request, 'bidcheckoutpage.html',
                          {'total_cart_price': bid["offer"], 'product': product, 'quantity': bid["quantity"], 'bid_id': bid_id, 'storename': bid["storename"]})
        else:
            messages.error(request, "Error loading checkout page - " + str(actionRes.getReturnValue()))
            return redirect('mainApp:mainpage')
    else:
        messages.error(request, "You must be logged in to checkout")
        return HttpResponseRedirect('/login')


@login_required(login_url='/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkoutpage(request):
    if request.user.is_authenticated:
        service = Service()
        res = service.getCart(request.user.username)
        if res.getStatus():
            cart = res.getReturnValue()
            baskets = ast.literal_eval(str(cart)).get('baskets')
            baskets = ast.literal_eval(str(baskets))
            products = []
            total_cart_price = 0
            quantity = 0
            for basket in baskets:
                basket_res = service.getBasket(request.user.username, basket)
                if basket_res.getStatus() == True:
                    basket_res = basket_res.getReturnValue()
                    basket_products = ast.literal_eval(str(basket_res)).get('products')
                    basket_products = ast.literal_eval(str(basket_products))
                    # for product in basket_products.values():
                    #     product['product'] = json.loads(product['product'])
                    total_cart_price += calculate_total_price(basket_products)
                    quantity += len(basket_products)
                    products.append(basket_products)

            return render(request, 'checkoutpage.html',
                          {'total_cart_price': total_cart_price, 'products': products, 'quantity': quantity})
        else:
            messages.error(request, "Error loading checkout page - " + str(res.getReturnValue()))
            return redirect('mainApp:mainpage')
    else:
        messages.error(request, "You must be logged in to checkout")
        return HttpResponseRedirect('/login')


@login_required(login_url='/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            service = Service()
            form = CheckoutForm(request.POST)
            if form.is_valid():
                res = service.purchaseCart(request.user.username, int(form.cleaned_data['cc_number']),
                                           form.cleaned_data['cc_expiration'], form.cleaned_data['cc_name'],
                                           int(form.cleaned_data['cc_cvv']), int(form.cleaned_data['cc_id']),
                                           form.cleaned_data['address'], form.cleaned_data['city'],
                                           form.cleaned_data['country'], int(form.cleaned_data['zip']))
                if res.getStatus():
                    messages.success(request,"Order placed successfully! thank you for shopping with us")

                    return redirect('mainApp:mainpage')
                else:
                    messages.error(request, "Error placing order res - " + str(res.getReturnValue()))
                    return HttpResponseRedirect('/cart')
            else:
                messages.error(request, "Error placing order form - " + str(form.errors))
                return HttpResponseRedirect('/cart')
        else:
            messages.error(request, "You must be logged in to place an order")
            return HttpResponseRedirect('/login')
    else:
        form = BasketEditProductForm()
        messages.error(request, "Error placing an order - " + str(request.method))
        return HttpResponseRedirect('/cart')

@login_required(login_url='/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkout_bid(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            service = Service()
            form = CheckoutForm(request.POST)
            if form.is_valid():
                bid_id = request.POST.get('bid_id')
                storename = request.POST.get('storename')
                res = service.purchaseConfirmedBid(bid_id, storename, request.user.username, int(form.cleaned_data['cc_number']),
                                           form.cleaned_data['cc_expiration'], form.cleaned_data['cc_name'],
                                           int(form.cleaned_data['cc_cvv']), int(form.cleaned_data['cc_id']),
                                           form.cleaned_data['address'], form.cleaned_data['city'],
                                           form.cleaned_data['country'], int(form.cleaned_data['zip']))
                if res.getStatus():
                    messages.success(request,"Bid has been purchased successfully! thank you for shopping with us")

                    return redirect('mainApp:mainpage')
                else:
                    messages.error(request, "Error placing order res - " + str(res.getReturnValue()))
                    return HttpResponseRedirect('/cart')
            else:
                messages.error(request, "Error placing order form - " + str(form.errors))
                return HttpResponseRedirect('/cart')
        else:
            messages.error(request, "You must be logged in to place an order")
            return HttpResponseRedirect('/login')
    else:
        form = BasketEditProductForm()
        messages.error(request, "Error placing an order - " + str(request.method))
        return HttpResponseRedirect('/cart')


def add_product_to_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            service = Service()
            form = BasketAddProductForm(request.POST)
            if form.is_valid():
                store = form.cleaned_data['store_name']
                product_id = form.cleaned_data['product_id']
                quantity = form.cleaned_data['quantity']
                res = service.addToBasket(request.user.username, store, product_id, quantity)
                if res.getStatus():
                    messages.success(request, "Product added successfully")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.error(request, "Error adding product to cart res - " + str(res.getReturnValue()))
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, "Error adding product to cart form - " + str(form.errors))
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "You must be logged in to add products to cart")
            return HttpResponseRedirect('/login')
    else:
        return redirect('mainApp:mainpage')


# -------------------------------------------------------Purchase History----------------------------------------------------------------#

@login_required(login_url='/login')
def userPurchaseHistory(request):
    if request.user.is_authenticated:
        service = Service()
        purchasehistory = service.getMemberPurchaseHistory(request.user.username,request.user.username)
        if purchasehistory.getStatus():
            purchasehistory = purchasehistory.getReturnValue()
            purchasehistory = ast.literal_eval(str(purchasehistory))
            return render(request, 'userPurchaseHistory.html',{'purchaseList': purchasehistory})
        else:
            messages.error(request, "Error: " + str(purchasehistory.getReturnValue()))
            return redirect('mainApp:cart')
    else:
        messages.error(request, "Error: User not authenticated")
        return redirect('mainApp:mainpage')



# -------------------------------------------------------Searchbar functionality---------------------------------------------------------#

def searchpage(request):
    if request.method == "POST":
        service = Service()
        searched = request.POST['searched']
        res = service.productSearchByName(searched, request.user.username)
        if res.getStatus():
            products= {}
            res_products = res.getReturnValue()
            for storeName, json_product_list in res_products.items():
                product_list =[]
                for product in json_product_list:
                    product = json.loads(product)
                    product_list.append(product)
                products[storeName] = product_list

            return render(request, 'searchpage.html', {'searched': searched, 'products': products})
        else:
            messages.error(request, "Error searching for products - " + str(res.getReturnValue()))
            return redirect('mainApp:mainpage')
    else:
        return redirect('mainApp:mainpage')


# ---------------------------------------------------------------------------------------------------------------------------------------#


# -----------------------------------------------------------Helper Functions------------------------------------------------------------#

def getDiscountType(discount):
    discount = int(discount)
    if discount == 1: return "Simple"
    if discount == 2: return "Conditioned"
    if discount == 3: return "Coupon"
    if discount == 4: return "Max"
    else: return "Add"


def getPurchasePolicyType(policy):
    # TODO: fix this when Amiel answers
    policy = int(policy)
    if policy == 1: return "PurchasePolicy"
    if policy == 2: return "todo2"
    if policy == 3: return "todo3"
    if policy == 4:
        return "todo4"
    else:
        return "todo5"


def getDiscountLevelType(level):
    level = int(level)
    if level == 1: return "Store"
    if level == 2:
        return "Category"
    else:
        return "Product"


def getPolicyLevelType(level):
    # TODO: fix this when Amiel answers
    level = int(level)
    if level == 1: return "Product"
    if level == 2: return "Category"
    if level == 3:
        return "User"
    else:
        return "Basket"


def getlevelName(level, name):
    level = int(level)
    if level == 1:
        return ""
    else:
        return name

def fixDiscountSpecial(discounts):
    new_dict = {}
    for key, value in discounts.items():
        new_key = str(key)
        new_dict[new_key] = value
    return new_dict


def fixDiscountRulesData(rulesData):
    keys = list(rulesData.keys())
    print(rulesData)
    if len(rulesData.keys()) == 1:
        print(f"len: {rulesData[0]}")
    for i in range(1, len(keys)):
        key = keys[i]
        previous_key = keys[i - 1]
        child_dict = {
            'logic_type': rulesData[key].pop('logic_type', ''),
            'rule': rulesData[key]
        }
        rulesData[previous_key]['child'] = child_dict
    rulesData[0].pop('logic_type', None)
    return rulesData[0]

    # TODO: check 2 lines:
    # rulesData["0"].pop('logic_type', None)
    # return rulesData["0"]

    # keys = list(rulesData.keys())
    # for i in range(1, len(keys)):
    #     prev_key = str(i - 1)
    #     current_key = str(i)
    #     rulesData[prev_key]['child'] = rulesData[current_key]
    # return rulesData['0']


def permissionCheck(username, storename, permissionName):
    if username == "": return False
    service = Service()
    permissions = service.getPermissionsAsJson(storename, username).getReturnValue()
    permissions: dict = ast.literal_eval(str(permissions))  # already a dict
    if permissionName in permissions.keys():
        return True
    return False


# returns False if user authenticated. Otherwise creates a new guest user and returns the username
def createGuestIfNeeded(request):
    if request.user.is_authenticated:
        return False

    # user needs to be guest
    # 1. create a new user in django
    # 2. login to that user
    else:
        service = Service()
        actionRes = service.loginAsGuest()

        if actionRes.getStatus():
            guestnumberdict = ast.literal_eval(str(actionRes.getReturnValue()))
            # form = CreateMemberForm(request.POST)
            username = f"GuestUser{guestnumberdict['entrance_id']}"
            password = "asdf1233"
            # email = "guestmail@guest.com"
            # form.save()
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                user.save()
            user = authenticate(request, username=username, password=password)
            loginFunc(request, user)
            request.session['guest'] = 1
            return username


# guest logges in as a user
# 1. change guest to user in service
# 2. logout of django
# 3. login as the user in django
# 4. remove the guest user from django
# returns False if current user not a guest. Otherwise logges in as member and returns the username
def guestToUser(request, username, password):
    guestusername = request.user.username
    if request.user.is_authenticated and request.session['guest']:
        service = Service()
        guestnumber = get_number_at_end(guestusername)
        actionRes = service.logInFromGuestToMember(guestnumber, username, password)  # 1.
        if actionRes.getStatus():
            logoutFunc(request)  # 2.
            user = authenticate(request, username=username, password=password)
            loginFunc(request, user)  # 3.
            guestuser = User.objects.get(username=guestusername)
            guestuser.delete()  # 4.
            request.session['guest'] = 0
            return username
            # ret = ast.literal_eval(str(actionRes.getReturnValue()))
            # return ret['entrance_id']

    return False


def get_number_at_end(string):
    number = ""
    for char in string[::-1]:
        if char.isdigit():
            number = char + number
        else:
            break
    return int(number)

#---------------------------------------------------------------------------------------------------------------------------------------#
