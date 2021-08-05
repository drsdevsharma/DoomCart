from django.shortcuts import render,redirect
from .models import Product, Cart,OrderPlaced
from user.models import Customer
from django.views import View
from django.db.models import Q
from django.http import JsonResponse



# ! Function 

# * function for total cost and other parameters 
# ! Start
def total_cost (cart,request):
    totalAmount = 0.0
    shippingCost = 0.0
    for product in cart:
        amount = product.product.discountPrice * product.quantity
        totalAmount += amount
    
    amount = totalAmount
    
    if totalAmount < 500.0 and totalAmount != 0.0:
        shippingCost = 70.0
        totalAmount += shippingCost
    cart_value = []
    if request.user.is_authenticated:
        cart_value = list(Cart.objects.filter(customer = request.user))

    return amount, totalAmount, shippingCost, cart_value
    
# ! End     


# * Check if product is already in cart if not then adds
# ! Start
def add_cart(product ,user):
    try: # * if product is already in cart then increase quantity else add to cart
        cart = Cart.objects.get(product = product)
    except Cart.DoesNotExist:
        cart = Cart(customer=user, product=product)
        cart.save()
    else:
        cart.quantity +=1
        cart.save()
# ! End
    





# Create your views here.


# * Show details of a product  
class ProductDetailsView(View ):
    def get(self, request , id):
        cart_value = []
        if request.user.is_authenticated:
            cart_value = list(Cart.objects.filter(customer = request.user))# * list of item in cart for sending the no. of items
        
        product = Product.objects.get(id = id)
        return render(request , 'product_details.html' , {'product': product ,'cart_value': len(cart_value)})


# * Show product of a specific category
class ProductCategoryView(View):
    brands = []
    def get(self, request , category):
        self.brands.clear()
        cart_value = []
        products = Product.objects.filter(category=category)
        for product in products:
            if product.brand not in self.brands: # * Adding barnds to the list
                self.brands.append(product.brand)
        if request.user.is_authenticated:
            cart_value = list(Cart.objects.filter(customer = request.user)) 

        return render(request, 'products.html', {'products': products,'brands': self.brands , 'category':category,'cart_value': len(cart_value)})


# * Show product of a specific brand
class BrandProductView(ProductCategoryView):
    def get (self, request,brand,category): 
        cart_value = []
        products = Product.objects.filter(category = category).filter( brand = brand) 
        if request.user.is_authenticated:
            cart_value = list(Cart.objects.filter(customer = request.user))
        
        return render(request, 'products.html', {'products': products,'brands': self.brands ,'category': category,'cart_value': len(cart_value)})




# * Add product to cart and redirect to checkout
class BuyNowView (View):
    def get(self, request ,id):
        if request.user.is_authenticated:
            user = request.user
            product = Product.objects.get(id=id)
            add_cart(product, user)
            customer = Customer.objects.filter(user= request.user)
            cart = Cart.objects.filter(customer=request.user)
            amount , totalAmount , shippingCost ,cart_value = total_cost(cart,request)
            if not customer:
                return redirect('add_profile') 
            
            return render(request,'checkout.html',{'Customer': customer,'Cart':cart,'shippingCost': shippingCost, 'totalAmount': totalAmount,'amount':amount,'cart_value': len(cart_value)}) 
        else:
            return redirect('/accounts/login/')



# * Add Product to cart
class AddToCartView(View):
    def get(self, request,id):
        if request.user.is_authenticated:
            user = request.user
            product = Product.objects.get(id=id)
            add_cart(product , user)
            return redirect('/product/show_cart/')
            
        else :
            return redirect('/accounts/login/')

# * Display the items in the cart
def ShowCart(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    cart_value = list(Cart.objects.filter(customer = request.user))
    user = request.user
    cart = Cart.objects.filter(customer=user)
    amount , totalAmount , shippingCost ,cart_value = total_cost(cart,request)
    for products in cart:
        products.product.discountPrice = products.product.discountPrice * products.quantity
    return render(request, 'add_to_cart.html' , {'Cart': cart,'totalAmount': totalAmount,'shippingCost': shippingCost,'amount': amount,'cart_value': len(cart_value)})


# * Increase the quantity of product
class PlusCartView(View):
    def get(self, request):
        id = request.GET['id']
        product = Product.objects.get(id=id)
        cart = Cart.objects.get(Q(product = product) & Q(customer = request.user))
        cart.quantity += 1
        quantity = cart.quantity
        productAmount = cart.product.discountPrice * quantity
        cart.save()
        cart = Cart.objects.filter(customer=request.user)
        amount , totalAmount , shippingCost ,cart_value = total_cost(cart,request)
        data = {
            'amount': amount,
            'totalAmount' : totalAmount,
            'quantity': quantity,
            'productAmount':productAmount
            }
        return JsonResponse (data)

    #* Decrease the quantity   of a product   
class MinusCartView(View):
    def get(self, request):
        
        id = request.GET['id']
        product = Product.objects.get(id=id)
        cart = Cart.objects.get(Q(product = product) & Q(customer = request.user))
        cart.quantity -= 1
        quantity = cart.quantity
        productAmount = cart.product.discountPrice * quantity
        if cart.quantity == 0:
            cart.delete()
        else:
            cart.save()
        cart = Cart.objects.filter(customer=request.user)
        amount , totalAmount , shippingCost ,cart_value = total_cost(cart,request)
        data = {
            'cart_value': len(cart_value),
            'amount': amount,
            'totalAmount' : totalAmount,
            'shippingCost': shippingCost,
            'quantity': quantity,
            'productAmount': productAmount
            }
        return JsonResponse (data)
        
# * Remove product form cart
class RemoveCartView(View):
    def get(self, request):
        id = request.GET['id']
        product = Product.objects.get(id=id)
        cart = Cart.objects.get(Q(product = product) & Q(customer = request.user))
        cart.delete()
        cart = Cart.objects.filter(customer=request.user)
        amount , totalAmount , shippingCost ,cart_value = total_cost(cart,request)
        data = {
            'cart_value':len(cart_value),
            'amount': amount,
            'totalAmount' : totalAmount,
            'shippingCost': shippingCost,
            }
        return JsonResponse (data)
       

# * Display CheckOut
class CheckOutView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')

        customer = Customer.objects.filter(user= request.user)
        if not customer:
            return redirect('add_profile')
        cart = Cart.objects.filter(customer= request.user)
        amount , totalAmount , shippingCost ,cart_value = total_cost(cart,request)   

        return render(request,'checkout.html',{'Customer': customer,'Cart':cart,'shippingCost': shippingCost, 'totalAmount': totalAmount,'amount':amount,'cart_value': len(cart_value)})

# * After payment add products to orders and remove products from cart
class PaymentView(View):
    def post(self, request):
        if request.user.is_authenticated:

            id = request.POST.get('id')
            if id:
                customer =Customer.objects.get(id=id)
                cart = Cart.objects.filter(customer=request.user)
                for item in cart:
                    OrderPlaced(user=request.user,product=item.product,customer=customer,quantity=item.quantity).save()
                    item.delete()
                return redirect('orders')
            else:
                return redirect('checkout')


# * Display Orders
class OrderView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart_value = list(Cart.objects.filter(customer = request.user))
        
            order = OrderPlaced.objects.filter(user=request.user)
            return render(request, 'orders.html', {'orders': order,'cart_value': len(cart_value)})
        else:
            return redirect('/accounts/login/')
