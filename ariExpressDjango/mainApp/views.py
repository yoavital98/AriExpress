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
from django.http import HttpResponseRedirect # for redirecting to another page and clearing the input fields
from django.contrib import messages # for displaying messages
from django.core.paginator import Paginator # for pagination
from datetime import datetime #used to get total msg per day
from django.views.decorators.cache import cache_control # for disabling cache



def startpage(request):
    return render(request, "startpage.html")

def mainpage(request):
    createGuestIfNeeded(request)
    return render(request, 'mainpage.html')

def login(request):
    msg = ""
    showMsg = False
    if request.method == 'POST':
        if request.user.is_authenticated and not request.session['guest']:
            msg="A User is already logged in"
            form = None
        else:
            service = Service()
            form = loginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                if request.session['guest']:
                    res = service.logIn(username, password)
                    msg = res.getStatus()
                    if res.getStatus() == True:
                        if not request.session['guest']:                                    # regular login
                            user = authenticate(request, username=username, password=password)
                            msg="Logged in successfully"
                            loginFunc(request, user)
                            request.session['guest'] = 0
                            return redirect('mainApp:mainpage')
                        else:                                                               # guest to member login
                            loggedin_username = guestToUser(request, username, password)
                            if loggedin_username: return loggedin_username
                            else: return False                                              # shouldn't happen
                        
                else:
                    guestToUser(request, username, password)
                    return redirect('mainApp:mainpage')

    else:
        form = loginForm()
        msg = ""
        showMsg = True


    return render(request, 'login.html', {'form': form,
                                          'msg': msg,
                                          'showMsg': showMsg})



def registerPage(request):
    msg = ""
    showMsg = False
    if request.method == 'POST':
        service = Service()
        if request.user.is_authenticated:
            msg="A User is already logged in"
            form = None
        else:
            form = CreateMemberForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                email = form.cleaned_data['email']
                res = service.register(username, password, email)
                msg = res.getReturnValue()
                if res.getStatus() == True:
                    form.save()
                    user = authenticate(request, username=username, password=password)
                    loginFunc(request, user)
                    request.session['guest'] = 0
                    return redirect('mainApp:mainpage')


    else:
        form = CreateMemberForm()
        msg = ""
        showMsg = True


    return render(request, 'register.html', {'form': form,
                                          'msg': msg,
                                          'showMsg': showMsg})


def logout(request):
    # if request.user.is_authenticated and not request.user.username.startswith("GuestUser"):
    if request.user.is_authenticated and not request.session['guest']:
        service = Service()
        actionRes = service.logOut(request.user.username)
        if actionRes.getStatus():
            logoutFunc(request)
            request.session['guest'] = 0
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
        # print(storesInfoDict)
        return render(request, 'mystores.html', {'stores': storesInfoDict})
    messages.success(request, ("Error: User is not logged in (django error)"))
    return redirect('mainApp:mainpage')



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
    else: permissions = {}

    print(permissions)
    print(storename)
    print(username)

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
        active = "Open" if context['active'].lower() == "true" else "Closed"
        return render(request, 'store_specific.html', {'products': products_dict, 'storename': storename, 'active': active, 'permissions': permissions})  
    # else:
    #     return redirect('mainApp:mainpage')
    

# def openStore(request, storename):
#     if request.method == 'POST' and request.user.is_authenticated:
#         service = Service()
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
#         service = Service()
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
            actionRes = service.editProductOfStore(request.user.username, storename, product_id, name=product_name, quantity=product_quantity, price=product_price, categories=product_categories)
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

def addNewDiscount(request, storename): # Discounts
    username = request.user.username
    permissionName = 'Discounts'
    if permissionCheck(username, storename, permissionName):
        discountTypeInt = None if request.POST.get('discountType') == None else int(request.POST.get('discountType'))
        discountType = None if discountTypeInt == None else getDiscountType(discountTypeInt)
        percent = 50 if request.POST.get('discountAmountRange') == None else int(request.POST.get('discountAmountRange'))
        levelTypeInt = None if request.POST.get('levelType') == None else int(request.POST.get('levelType'))
        levelType = None if levelTypeInt == None else getLevelType(levelTypeInt)
        levelName = None if request.POST.get('levelName') == None else request.POST.get('levelName')

        if 'submitDiscount' in request.POST:
            service = Service()
            if discountTypeInt == 1:
                actionRes = service.addDiscount(storename, username, discountType, percent, levelType, levelName)
                if actionRes.getStatus():
                    messages.success(request, ("Discount has been added"))
                else:
                    messages.success(request, (f"Error: {actionRes.getReturnValue()}"))


            if discountTypeInt == 2:
                rulesData = request.session['rulesData']
                fixedRulesData = fixRulesData(rulesData)
                actionRes = service.addDiscount(storename, username, discountType, percent, levelType, levelName, fixedRulesData)
                if actionRes.getStatus():
                    messages.success(request, ("Discount has been added"))
                    if 'rulesData' in request.session:
                        del request.session['rulesData']
                else:
                    messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
                

            if discountTypeInt == 3:
                pass

            if discountTypeInt == 4:
                pass

            if discountTypeInt == 5:
                pass


        if 'conditionedAddRule' in request.POST:
            # Retrieve the submitted rulesData
            rulesData = request.POST.get('rulesData')
            ruleData = json.loads(rulesData)

            if 'rulesData' not in request.session:
                request.session['rulesData'] = {}
                request.session['ruleCounter'] = 0

            # Check if ruleData is not already in the session
            if ruleData not in dict(request.session['rulesData']).values():
                counter = request.session['ruleCounter']
                ruleDict = request.session['rulesData']
                ruleDict[counter] = ruleData
                request.session['ruleCounter'] += 1


        if 'clearAllRules' in request.POST:
            if 'rulesData' in request.session:
                del request.session['rulesData']
            request.session['ruleCounter'] = 0

        return render(request, 'addNewDiscount.html', {'storename': storename, 'percent': percent, 'discountType': discountType, 'levelType': levelType, 'levelName': levelName})
    else:
        messages.success(request, (f"Error: {username} doesn't have {permissionName} permission"))
        return redirect('mainApp:store_specific', storename=storename)

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
                return render(request, 'nominateUser.html', {'storename': storename})           #didn't nominate yet, just load the page


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
                actionRes = service.addNewProductToStore(request.user.username, storename, productname, category, quantity, price)
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
                onlinemembers = resOnline.getReturnValue() #returns a list
                offlinemembers = resOffline.getReturnValue() #returns a list
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
    all_user_messages = UserMessage.objects.filter(receiver=request.user.username).order_by('-creation_date')
    pending = UserMessage.objects.filter(receiver=request.user.username, status='pending').count()
    paginator = Paginator(all_user_messages, 5)
    page = request.GET.get('page')
    all_messages = paginator.get_page(page)
    return render(request, 'inbox.html',{'usermessages': all_messages, 'pending': pending})


def send_message(request):
    if request.method == 'POST':
        service = Service()
        form = UserMessageform(request.POST, request.FILES)
        if form.is_valid():
            receiver_username = form.cleaned_data['receiver']
            res = service.checkUsernameExistence(receiver_username)
            if res.getStatus():
                message = form.save(commit=False)
                message.sender = request.user.username
                message.save()
                messages.success(request, "Message sent successfully")
                return HttpResponseRedirect('/inbox')
            else:
                messages.error(request, "Invalid adresssee username - the message was not sent")
        else:
            messages.error(request, "Invalid form submission")
    else:
        form = UserMessageform()
        messages.error(request, "Error sending message")
    return HttpResponseRedirect('/inbox')   


@login_required(login_url='/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_message(request, usermessage_id):
    message = UserMessage.objects.get(id=usermessage_id)
    message.delete()
    messages.success(request, "Message deleted successfully")
    return HttpResponseRedirect('/inbox')



@login_required(login_url='/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mark_as_read(request, usermessage_id):
    message = UserMessage.objects.get(id=usermessage_id)
    message.status = 'read'
    message.save()
    messages.success(request, "Message marked as read successfully")
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

@login_required(login_url='/login')
def notifications(request):
    pending = UserMessage.objects.filter(receiver=request.user.username, status='pending').count()



#---------------------------------------------------------cart functionality---------------------------------------------------------#
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
        messages.error(request, "Error removing product from cart - "+ str(request.method))
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
        messages.error(request, "Error editting product quantity - "+ str(request.method))
        return HttpResponseRedirect('/cart')  
    

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
            total_cart_price=0
            quantity= 0
            for basket in baskets:
                basket_res = service.getBasket(request.user.username, basket)
                if basket_res.getStatus() == True:
                    basket_res = basket_res.getReturnValue()
                    basket_products = ast.literal_eval(str(basket_res)).get('products')
                    basket_products = ast.literal_eval(str(basket_products))
                    total_cart_price += calculate_total_price(basket_products)
                    quantity += len(basket_products)
                    products.append(basket_products)

            return render(request, 'checkoutpage.html', {'total_cart_price': total_cart_price, 'products': products, 'quantity': quantity})
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
                full_address = str(form.cleaned_data['address'])+", "+str(form.cleaned_data['country'])
                res = service.purchaseCart(request.user.username, int(form.cleaned_data['cc_number']), form.cleaned_data['cc_name'], int(form.cleaned_data['cc_id']), form.cleaned_data['cc_expiration'], int(form.cleaned_data['cc_cvv']), full_address)
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
        messages.error(request, "Error placing an order - "+ str(request.method))
        return HttpResponseRedirect('/cart')  

def add_product_to_cart(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            service = Service()
            form = BasketAddProductForm(request.POST)
            if form.is_valid():
                store = form.cleaned_data['store_name']
                product_id = form.cleaned_data['product_id']
                quantity = form.cleaned_data['quantity']
                searched = form.cleaned_data['searched']
                res = service.addToBasket(request.user.username, store, product_id, quantity)
                if res.getStatus():
                    messages.success(request, "Product added successfully")
                    return searchpage(request)
                else:
                    messages.error(request, "Error adding product to cart res - " + str(res.getReturnValue()))
                    return searchpage(request)
            else:
                messages.error(request, "Error adding product to cart form - " + str(form.errors))
                return searchpage(request)
        else:
            messages.error(request, "You must be logged in to add products to cart")
            return HttpResponseRedirect('/login')
    else:
        return redirect('mainApp:mainpage')

#---------------------------------------------------------------------------------------------------------------------------------------#



#-------------------------------------------------------Searchbar functionality---------------------------------------------------------#

def searchpage(request):
    if request.method == "POST":
        service = Service()
        searched = request.POST['searched']
        res = service.productSearchByName(searched,request.user.username)
        if res.getStatus():
            products = res.getReturnValue()
            return render(request, 'searchpage.html', {'searched': searched, 'products': products})
        else:
            messages.error(request, "Error searching for products - " + str(res.getReturnValue()))
            return redirect('mainApp:mainpage')
    else:
        return redirect('mainApp:mainpage')


#---------------------------------------------------------------------------------------------------------------------------------------#




#-----------------------------------------------------------Helper Functions------------------------------------------------------------#

def getDiscountType(discount):
    discount = int(discount)
    if discount == 1: return "Simple"
    if discount == 2: return "Conditioned"
    if discount == 3: return "Coupon"
    if discount == 4: return "Max"
    else: return "Add"

def getLevelType(level):
    level = int(level)
    if level == 1: return "Store"
    if level == 2: return "Category"
    else: return "Product"

def getlevelName(level, name):
    level = int(level)
    if level == 1: return ""
    else: return name

def fixRulesData(rulesData):
    keys = list(rulesData.keys())
    for i in range(1, len(keys)):
        key = keys[i]
        previous_key = keys[i-1]
        child_dict = {
            'logic_type': rulesData[key].pop('logic_type', ''),
            'rule': rulesData[key]
        }
        rulesData[previous_key]['child'] = child_dict
    rulesData['0'].pop('logic_type', None)
    return rulesData['0']

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
    permissions : dict = ast.literal_eval(str(permissions))                             #already a dict
    if permissionName in permissions.keys():
        return True
    return False

#returns False if user authenticated. Otherwise creates a new guest user and returns the username
def createGuestIfNeeded(request):
    if request.user.is_authenticated:
        return False

    
    # user needs to be guest
    # 1. create a new user in django
    # 2. login to that user
    else:   
        service = Service()
        actionRes = service.loginAsGuest()
        guestnumberdict = ast.literal_eval(str(actionRes.getReturnValue()))

        if actionRes.getStatus():
            # form = CreateMemberForm(request.POST)
            username = f"GuestUser{guestnumberdict['entrance_id']}"
            password = "asdf1233"
            # email = "guestmail@guest.com"
            # form.save()
            user = User.objects.create_user(username=username, password=password)
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
        print(f"guestnumber: {guestnumber}")
        actionRes = service.logInFromGuestToMember(guestnumber, username, password) # 1.
        if actionRes.getStatus():
            logoutFunc(request)                                                     # 2.
            user = authenticate(request, username=username, password=password)      
            loginFunc(request, user)                                                # 3.
            guestuser = User.objects.get(username=guestusername)
            guestuser.delete()                                                      # 4.
            request.session['guest'] = 1
            print(f"guest: {request.session['guest']}")
            ret = ast.literal_eval(str(actionRes.getReturnValue()))
            return ret['entrance_id']

    else: return False


def get_number_at_end(string):
    number = ""
    for char in string[::-1]:
        if char.isdigit():
            number = char + number
        else:
            break
    return int(number)
#---------------------------------------------------------------------------------------------------------------------------------------#