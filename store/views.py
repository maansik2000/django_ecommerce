from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

# Create your views here.
def store(request):
    
    data = cartData(request)
    cartItems = data['cartItems']

        
    products = Product.objects.all()                                            #get all the products from the backend
    context = {'products' : products,'cartItems' : cartItems,'shipping' : False } #store all the product in this context and then send it to the template
    return render(request, 'store/store.html',context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order'] 
    items = data['items']

    context = {'items':items,'order' : order,'cartItems' : cartItems,'shipping' : False }
    return render(request,'store/cart.html',context)



def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'items':items,'order' : order,'cartItems' : cartItems,'shipping' : False }
    return render(request,'store/checkout.html',context)


 #backend where product is sent
def updateItem(request):                                   
    data = json.loads(request.body)                                             #get the data from the backend using the post request and parse into the json object
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    
    customer = request.user.customer                                            #create the user for the customer
    product = Product.objects.get(id=productId)                                 #get the product using the product id
    order, created = Order.objects.get_or_create(customer=customer, complete=False)  #order is created

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)  #if the order item already exist there is no need to create a new one
    
    if action == 'add':                                                         #if the action is add, increase the quantity 
    		orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':                                                    #otherwise decrement
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()                                                            #save the orderitem in the cart

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was added', safe = False)                         #send the respose data


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data) 
        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

    return JsonResponse('Payment submitted..', safe=False)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request,'store/login.html',context )


def register(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'Account is created for '+ user)
                
                return redirect('loginUser')
            
        context = {'form' : form}
        return render(request,'store/signup.html',context)


def logoutUser(request):
    logout(request)
    return redirect('loginPage')