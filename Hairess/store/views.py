from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout 
#from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from random import randint
from django.http import JsonResponse
import json
from .models import *
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(customer_name = request.user.customer)#get customer when logged in
        order = Order.objects.filter(customer = customer)#Signed in user
        
    else:
        try:

            customer = Customer.objects.get(device_id = request.COOKIES['device'])

        except:
            customer_create = Customer.objects.get_or_create(device_id = request.COOKIES['device'])
            customer = Customer.objects.get(device_id = request.COOKIES['device']) #get customer by device_id when not logged in

        order = Order.objects.filter(customer = customer) #Guest user 

        
    try:
        user = User.objects.get(username = request.user)
    except:
        user = None
        
    products = Product.objects.all()
    context = {'products' : products,
               'user' : user,
               'order' : order
               }    
    return render(request,"store/index.html", context)

def cart(request):
    
    if request.user.is_authenticated:
        customer = Customer.objects.get(customer_name = request.user.customer)#get customer when logged in
        items = OrderItem.objects.filter(customer = customer) #Signed in user
        order = Order.objects.filter(customer = customer)

    else:
        try:

            customer = Customer.objects.get(device_id = request.COOKIES['device'])

        except:

            customer_create = Customer.objects.get_or_create(device_id = request.COOKIES['device'])
            customer = Customer.objects.get(device_id = request.COOKIES['device']) #get customer by device_id when not logged in

        items = OrderItem.objects.filter(customer = customer) #Guest user
        order = Order.objects.filter(customer = customer)

    if request.method == 'POST':
        items.delete()#deletes everything in the orderitem model depending on the user
        order.delete()#deletes everything in the order model depending on the user
        
    try:
        user = User.objects.get(username = request.user)
    except:
        user = None

    context = {'items':items, 'order':order, 'user':user} 
    return render(request, "store/cart.html", context)

def checkout(request):
    """ if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_subtotal':0,'get_cart_items':0}
        
    context = {'items':items,'order':order} """
    if request.user.is_authenticated:
        customer = Customer.objects.get(customer_name = request.user.customer)#get customer when logged in
        items = OrderItem.objects.filter(customer = customer) #Signed in user
        
    else:
        try:

            customer = Customer.objects.get(device_id = request.COOKIES['device'])

        except:
            customer_create = Customer.objects.get_or_create(device_id = request.COOKIES['device'])
            customer = Customer.objects.get(device_id = request.COOKIES['device']) #get customer by device_id when not logged in

        items = OrderItem.objects.filter(customer = customer) #Guest user 
        order = {'get_cart_subtotal':0,'get_cart_items':0}

        
    try:
        user = User.objects.get(username = request.user)
    except:
        user = None
        
    products = Product.objects.all()
    context = {
               'user' : user,
               'items' : items
               }    
    return render(request,"store/checkout.html",context)

def Apicart(request):
    
    data = json.loads(request.body)#converts json data to dictionary
    productId = data['productId']
    action = data['action']
    cookie = request.COOKIES['device'] 
    print(productId, action)
    #userdata = data['user']
            
    #user = User.objects.get(username = userdata)
    try:
        customer = Customer.objects.get(customer_name = request.user.customer)
    
            
        if action == 'add':
            product = Product.objects.get(id = productId)
            print(product)
            try:

                additem = OrderItem.objects.get(customer = customer, product = product)
                additem.quantity += 1
                additem.save()

            except:

                try:
                    order_get = Order.objects.get(customer = customer)
                except:
                    order = Order.objects.get_or_create(customer = customer, product = product, complete = False, transaction_id = str(randint(1000,10000)))
                    order_get = Order.objects.get(customer = customer)
                orderitem = OrderItem.objects.get_or_create(customer = customer, product = product, order = order_get, quantity = 1) 

        elif action == 'plus':

                    
            orderitem = OrderItem.objects.get(id = productId)
            orderitem.quantity += 1
            orderitem.save()

        else:

            orderitem = OrderItem.objects.get(id = productId)
            orderitem.quantity -= 1
            orderitem.save()

            if orderitem.quantity == 0:
                orderitem.delete()

    except:

        customer_create = Customer.objects.get_or_create(device_id = cookie)
        customer = Customer.objects.get(device_id = cookie)

        if action == 'add':
            product = Product.objects.get(id = productId)
            try:

                additem = OrderItem.objects.get(customer = customer, product = product)
                additem.quantity += 1
                additem.save()

            except:

                try:
                    order_get = Order.objects.get(customer = customer)
                except:
                    order = Order.objects.get_or_create(customer = customer, product = product, complete = False, transaction_id = str(randint(1000,10000)))
                    order_get = Order.objects.get(customer = customer)
                orderitem = OrderItem.objects.get_or_create(customer = customer, product = product, order = order_get, quantity = 1) 

        elif action == 'plus':

                    
            orderitem = OrderItem.objects.get(id = productId)
            orderitem.quantity += 1
            orderitem.save()

        else:

            orderitem = OrderItem.objects.get(id = productId)
            orderitem.quantity -= 1
            orderitem.save()

            if orderitem.quantity == 0:
                orderitem.delete()

    
             
                               
    try:
        return JsonResponse('added to cart...', safe = False)
    except:
        return HttpResponse('oops something went wrong...')

def category(request):
    context = {}
    return render(request,"store/category.html",context)

def product_details(request, id):
    if request.user.is_authenticated:
        customer = Customer.objects.get(customer_name = request.user.customer)#get customer when logged in
        order = Order.objects.filter(customer = customer)#Signed in user
        
    else:
        try:

            customer = Customer.objects.get(device_id = request.COOKIES['device'])

        except:
            customer_create = Customer.objects.get_or_create(device_id = request.COOKIES['device'])
            customer = Customer.objects.get(device_id = request.COOKIES['device']) #get customer by device_id when not logged in

        order = Order.objects.filter(customer = customer)#Guest user 
    
    try:
        user = User.objects.get(username = request.user)
    except:
        user = None
    
    products = Product.objects.get(id = id)
    context = {'products':products,'user':user,'order':order}
    
    return render(request,"store/product.html",context)

def hair_bundles_products(request,id):
    if request.user.is_authenticated:
        customer = Customer.objects.get(customer_name = request.user.customer)#get customer when logged in
        items = OrderItem.objects.filter(customer = customer) #Signed in user
        
    else:
        try:

            customer = Customer.objects.get(device_id = request.COOKIES['device'])

        except:
            customer_create = Customer.objects.get_or_create(device_id = request.COOKIES['device'])
            customer = Customer.objects.get(device_id = request.COOKIES['device']) #get customer by device_id when not logged in

        items = OrderItem.objects.filter(customer = customer) #Guest user 
    
    try:
        user = User.objects.get(username = request.user)
    except:
        user = None
        
        
    products = Hair_bundles.objects.get(id=id)
    context = {'products':products,'items':items,'user':user}
    return render(request,"store/product.html",context)


def Register(request):

    value = randint(1,3000)
    email_check = []
    
    for i in Customer.objects.all():
        try:
            print(i.user.email)
            email_check.append(i.user.email)
        except:
            pass

    if request.method == 'POST':

        try:

            firstname = request.POST['firstname']   
            lastname = request.POST['lastname']
            password = request.POST['password']
            confirmpassword = request.POST['confirmpassword']
            email = request.POST['email']
            
            if email in email_check:
                check = True
                return render(request, 'store/signUp.html', {'check':'Email already exists.'})
            else:
                check = False
            
            #Create User
            if check == False:

                user = User.objects.create_user(username = firstname+str(value), first_name = firstname, last_name = lastname, password = password, email = email, is_staff=False, is_superuser=False)
                customer = Customer.objects.create(user = user, customer_name = firstname)
                #Login on User Created
                user_login = authenticate(request, username = User.objects.get(email = email).username, password = password)
                print(email,firstname,password,lastname)
                if user_login.is_authenticated:
                    auth_login(request,user_login)
                    return redirect('index')

        except Exception as e:
            raise e #raise error if there is one

    

    return render(request, 'store/signUp.html')

def Login(request):

    if request.method == 'POST':
        #Login user
        try:

            email = request.POST['email']
            password = request.POST['password']

            try:
                user = User.objects.get(email = email)
            except:
                return render(request, 'store/signIn.html', {'err' : "User doesn't exist."})

            try:
                user_login = authenticate(request, username = user.username, password = password)

                if user_login.is_authenticated:
                    auth_login(request,user_login)
                    return redirect('index')

            except :
                     return render(request, 'store/signIn.html', {'error' : "Incorrect password, Check your password."})

            

        except Exception as e:
            pass #raise error if there is one

    return render(request, 'store/signIn.html')

def Logout(request):
    logout(request)
    return redirect('index') 

def ForgotP(request):

    if request.method == 'POST':

        try:

            email = request.POST['email']
            #checks if there is a user with this email
            user = User.objects.get(email = email)
            return redirect('newpassword', email = email)

        except:

            return render(request, 'store/forgotpassword.html', {'err' : "User doesn't exist."})

    return render(request, 'store/forgotpassword.html')

def NewPassword(request, email):
    
    if request.method == 'POST':

        password = request.POST['password']
        confirm = request.POST['confirmpassword']

        if password == confirm:
            user = User.objects.get(email = email)
            user.set_password(password)
            user.save()
            return redirect('login')


    return  render(request, 'store/newpassword.html')  

def search(request):
    #search item
    searched_word = request.GET.get('q', False)#gets the searched word if there is none it returns false

    searchitem = Product.objects.filter(
        Q(name__icontains = searched_word) 
        )# searches the word in the database based on the product.name 
    print(searchitem)

    #Allows the cart quantity to be seen by the user in the search.html
    if request.user.is_authenticated:
        customer = Customer.objects.get(customer_name = request.user.customer)#get customer when logged in
        items = OrderItem.objects.filter(customer = customer) #Signed in user
        
    else:
        try:

            customer = Customer.objects.get(device_id = request.COOKIES['device'])

        except:
            customer_create = Customer.objects.get_or_create(device_id = request.COOKIES['device'])
            customer = Customer.objects.get(device_id = request.COOKIES['device']) #get customer by device_id when not logged in

        items = OrderItem.objects.filter(customer = customer)
    

    #Allows the user name to be seen by the user if there is one in the search.html
    try:
        user = User.objects.get(username = request.user)
    except:
        user = None

    context = {'searchitem' : searchitem, 'searched_word' : searched_word, 'user' : user, 'items' : items}

    return render(request, 'store/search.html', context)

def hair_bundles(request):
    
    if request.user.is_authenticated:
        customer = Customer.objects.get(customer_name = request.user.customer)#get customer when logged in
        items = OrderItem.objects.filter(customer = customer) #Signed in user
        
    else:
        try:

            customer = Customer.objects.get(device_id = request.COOKIES['device'])

        except:
            customer_create = Customer.objects.get_or_create(device_id = request.COOKIES['device'])
            customer = Customer.objects.get(device_id = request.COOKIES['device']) #get customer by device_id when not logged in

        items = OrderItem.objects.filter(customer = customer) #Guest user 

        
    try:
        user = User.objects.get(username = request.user)
    except:
        user = None
        
    products = Hair_bundles.objects.all()
    #context = {'products':products}
    
    paginator = Paginator(products,per_page=3)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    return render(request,
                  "store/hair_bundles.html",
                  {
                      'products':page_obj.object_list,
                      'paginator':paginator,
                      'page_number':int(page_number),
                      'user':user,
                      'items':items
                  }
    )