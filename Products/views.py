from django.shortcuts import render,redirect
from .models import Product, Cart,OrderPlaced
from user.models import Customer
from django.views import View
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.
class ProductDetailsView(View ):
    def get(self, request , id):
        cart_value = []
        if request.user.is_authenticated:
            cart_value = list(Cart.objects.filter(customer = request.user))
        
        product = Product.objects.get(id = id)
        return render(request , 'product_details.html' , {'product': product ,'cart_value': len(cart_value)})



class ProductCategoryView(View):
    brands = []
    def get(self, request , category):
        self.brands.clear()
        cart_value = []
        products = Product.objects.filter(category=category)
        for product in products:
            if not(product.brand in self.brands):
               self.brands.append(product.brand)
        if request.user.is_authenticated:
            cart_value = list(Cart.objects.filter(customer = request.user))
        
        return render(request, 'products.html', {'products': products,'brands': self.brands , 'category':category,'cart_value': len(cart_value)})


class BrandProductView(ProductCategoryView):
    def get (self, request,brand,category): 
        cart_value = []
        products = Product.objects.filter(category = category).filter( brand = brand) 
        if request.user.is_authenticated:
            cart_value = list(Cart.objects.filter(customer = request.user))
        
        return render(request, 'products.html', {'products': products,'brands': self.brands ,'category': category,'cart_value': len(cart_value)})


class BuyNowView(View):
    def get(self, request ,id):
        if request.user.is_authenticated:
            cart_value = list(Cart.objects.filter(customer = request.user))
            user = request.user
            product = Product.objects.get(id=id)
            customer = Customer.objects.filter(user= request.user)
            try:
                cart = Cart.objects.get(product = product)
            except Cart.DoesNotExist:
                cart = Cart(customer=user, product=product)
                cart.save()
            else:
                cart.quantity +=1
                cart.save()
            cart = Cart.objects.filter(customer=request.user)
            totalAmount = 0.0
            shippingCost = 0.0
            for product in cart:
                amount = product.product.discountPrice * product.quantity
                totalAmount += amount
            
            amount = totalAmount
            
            if totalAmount < 500.0 and totalAmount != 0.0:
                shippingCost = 70.0
                totalAmount += shippingCost
            if not customer:
                return redirect('add_profile') 
            
            return render(request,'checkout.html',{'Customer': customer,'Cart':cart,'shippingCost': shippingCost, 'totalAmount': totalAmount,'amount':amount,'cart_value': len(cart_value)}) 
        else:
            return redirect('/accounts/login/')




class AddToCartView(View):
    def get(self, request,id):
        if request.user.is_authenticated:
            user = request.user
            product = Product.objects.get(id=id)

            try:
                cart = Cart.objects.get(product = product)
            except Cart.DoesNotExist:
                cart = Cart(customer=user, product=product)
                cart.save()
            else:
                cart.quantity +=1
                cart.save()
            return redirect('/product/show_cart/')
            
        else :
            return redirect('/accounts/login/')


def ShowCart(request):
    if request.user.is_authenticated:
        cart_value = list(Cart.objects.filter(customer = request.user))
        user = request.user
        cart = Cart.objects.filter(customer=user)
        totalAmount = 0.0
        shippingCost = 0.0
        for product in cart:
            amount = product.product.discountPrice * product.quantity
            totalAmount += amount
        
        amount = totalAmount
        
        if totalAmount < 500.0 and totalAmount != 0.0:
            shippingCost = 70.0
            totalAmount += shippingCost
        return render(request, 'add_to_cart.html' , {'Cart': cart,'totalAmount': totalAmount,'shippingCost': shippingCost,'amount': amount,'cart_value': len(cart_value)})
    else:
        return redirect('/accounts/login/')



class PlusCartView(View):
    def get(self, request):
        id = request.GET['id']
        product = Product.objects.get(id=id)
        cart = Cart.objects.get(Q(product = product) & Q(customer = request.user))
        cart.quantity += 1
        quantity = cart.quantity
        cart.save()
        cart = Cart.objects.filter(customer=request.user)
        totalAmount = 0.0
        shippingCost = 0.0
        for product in cart:
            amount = product.product.discountPrice * product.quantity
            totalAmount += amount
        
        amount = totalAmount
        
        if totalAmount < 500.0 and totalAmount != 0.0:
            shippingCost = 70.0
            totalAmount += shippingCost
        data = {
            'amount': amount,
            'totalAmount' : totalAmount,
            'quantity': quantity
            }
        return JsonResponse (data)
        
class MinusCartView(View):
    def get(self, request):
        
        id = request.GET['id']
        product = Product.objects.get(id=id)
        cart = Cart.objects.get(Q(product = product) & Q(customer = request.user))
        cart.quantity -= 1
        quantity = cart.quantity
        if cart.quantity == 0:
            cart.delete()
        else:
            cart.save()
        cart = Cart.objects.filter(customer=request.user)
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
        
        data = {
            'cart_value': len(cart_value),
            'amount': amount,
            'totalAmount' : totalAmount,
            'shippingCost': shippingCost,
            'quantity': quantity
            }
        return JsonResponse (data)
        
class RemoveCartView(View):
    def get(self, request):
        id = request.GET['id']
        product = Product.objects.get(id=id)
        cart = Cart.objects.get(Q(product = product) & Q(customer = request.user))
        cart.delete()
        cart = Cart.objects.filter(customer=request.user)
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
        
        data = {
            'cart_value':len(cart_value),
            'amount': amount,
            'totalAmount' : totalAmount,
            'shippingCost': shippingCost,
            }
        return JsonResponse (data)
        
class CheckOutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart_value = list(Cart.objects.filter(customer = request.user))
            
            customer = Customer.objects.filter(user= request.user)
            if not customer:
                return redirect('add_profile')
            cart = Cart.objects.filter(customer= request.user)
            totalAmount = 0.0
            shippingCost = 0.0
            for product in cart:
                amount = product.product.discountPrice * product.quantity
                totalAmount += amount
            
            amount = totalAmount
            
            if totalAmount < 500.0 and totalAmount != 0.0:
                shippingCost = 70.0
                totalAmount += shippingCost
                
            return render(request,'checkout.html',{'Customer': customer,'Cart':cart,'shippingCost': shippingCost, 'totalAmount': totalAmount,'amount':amount,'cart_value': len(cart_value)}) 


        else:
            return redirect('/accounts/login/')


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


class OrderView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart_value = list(Cart.objects.filter(customer = request.user))
        
            order = OrderPlaced.objects.filter(user=request.user)
            return render(request, 'orders.html', {'orders': order,'cart_value': len(cart_value)})
        else:
            return redirect('/accounts/login/')
