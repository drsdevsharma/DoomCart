from django.shortcuts import render,redirect
from Products.models import Product,Cart
from django.views import View
from .forms import RegisterationForm,CustomerProfileForm
from django.contrib import messages
from .models import Customer


class HomeView(View):
    def get(self, request):
        cart_value = None
        mobiles = Product.objects.filter(category = 'mobile')
        laptops = Product.objects.filter(category = 'laptop')
        jeans = Product.objects.filter(category = 'jeans')
        shirts = Product.objects.filter(category = 'shirt')
        if request.user.is_authenticated:
            cart_value = list(Cart.objects.filter(customer = request.user))
            cart_value = len(cart_value)
        return render(request, 'home.html',
            {'mobiles':mobiles,'laptops':laptops,'jeans':jeans,'shirts':shirts,'cart_value':cart_value})



class RegisterationView(View):
    def get(self, request):
        form = RegisterationForm()
        return render(request,'register.html', {'form':form})


    def post(self, request):
        form = RegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'User registered successfully ')
            return redirect('/')
        return render(request, 'register.html', {'form': form})



class AddProfileView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            cart = list(Cart.objects.filter(customer = request.user))
        
        form = CustomerProfileForm()
        return render(request, 'address.html', {'form': form , 'cart_value': len(cart)})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if request.user.is_authenticated:
            cart = list(Cart.objects.filter(customer = request.user))
            
        if form.is_valid():
            data = {
                'user':request.user,
                'name': form.cleaned_data['name'],
                'loaclity': form.cleaned_data['loaclity'],
                'city': form.cleaned_data['city'],
                'state': form.cleaned_data['state'],
                'zipCode': form.cleaned_data['zipCode'],
                'phoneNumber': form.cleaned_data['phoneNumber']

            }
            customer = Customer(**data)
            customer.save()
            messages.success(request, 'Profile added successfully ')
            return redirect('/profile/')
    
        return render(request, 'address.html', {'form': form,'cart_value': len(cart)})
    


class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart = list(Cart.objects.filter(customer = request.user))
        
        CustomerProfile = Customer.objects.filter(user = request.user)
        return render(request, 'profile.html',{'Customer':CustomerProfile,'cart_value': len(cart)})
