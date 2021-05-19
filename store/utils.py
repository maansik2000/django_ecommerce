import json
from .models import *

def cookieCart(request):

	#Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])                              #gets the cookie and then parse the cookie cart into the json object
    except:
        cart = {} 
        print(cart)
        
    items = []
    order = {'get_cart_total' : 0,'get_cart_items' : 0}                     #set 0 to cart items and cart total if the user not logged in
    cartItems = order['get_cart_items']
    
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]                                    #get the quantity in the cart cookie
            
            product = Product.objects.get(id = i)
            
            total = (product.price * cart[i]["quantity"])
            order['get_cart_items'] += cart[i]['quantity']
            order['get_cart_total'] += total
            
            item = {
                'id':product.id,
                'product':{'id':product.id,'name':product.name, 'price':product.price, 
                'imageURL':product.imageURL}, 'quantity':cart[i]['quantity'],
                'digital':product.digital,'get_total':total,
                }
            items.append(item)
            
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
        
    return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
    if request.user.is_authenticated:                                           #check of the user is authenticated
        customer = request.user.customer                                        #make a user for the customer 
        order, created = Order.objects.get_or_create(customer = customer, complete=False)    #first it tries to get the order if it is not present then it will create a order
        items = order.orderitem_set.all()                                       #get all the orderItems / items from the cart
                                                                                #order is the parent, orderitem is the child of order that's how we will fetch the cart items
        cartItems = order.get_cart_items                                        #set the cart items logo = number of item in the cart
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems':cartItems ,'order':order, 'items':items}

	
def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
			email=email,
			)
	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for item in items:
		product = Product.objects.get(id=item['product']['id'])
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=item['quantity'],
		)
	return customer, order