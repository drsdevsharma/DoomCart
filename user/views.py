from django.shortcuts import render,redirect
from Products.models import Product,Cart
from django.views import View
from .forms import ForgotPasswordForm, RegisterationForm,CustomerProfileForm
from django.contrib import messages
from .models import Customer,UserProfile
import uuid
from django.conf import settings # For email related variables
from django.core.mail import send_mail # for sending email
from .message import Message
from django.contrib.auth.models import User



class HomeView(View):
    def get(self, request):
        cart_value = None
        mobiles = Product.objects.filter(category = 'mobile')
        laptops = Product.objects.filter(category = 'laptop')
        jeans = Product.objects.filter(category = 'jeans')
        shirts = Product.objects.filter(category = 'shirt')
        if request.user.is_authenticated and IsProfileVerified(request) :

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
            userObj = form.save()
            profileObj = UserProfile.objects.create(user = userObj,auth_token = str(uuid.uuid4()))
            profileObj.save()
            messages.success(request,'User registered successfully ')
            verifyEmail(userObj,userObj.email)
            return NotVerified(request)
        return render(request, 'register.html', {'form': form})



class AddProfileView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            if IsProfileVerified (request):
                cart = list(Cart.objects.filter(customer = request.user))
        
                form = CustomerProfileForm()
                return render(request, 'address.html', {'form': form , 'cart_value': len(cart)})
            NotVerified(request)
        return redirect('login')

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
        if request.user.is_authenticated and IsProfileVerified(request):
            cart = list(Cart.objects.filter(customer = request.user))
        
            CustomerProfile = Customer.objects.filter(user = request.user)
            return render(request, 'profile.html',{'Customer':CustomerProfile,'cart_value': len(cart)})
        return redirect('login')

def verifyEmail(user,email):
    profileObj = UserProfile.objects.get(user=user)
    message = Message(user,profileObj.auth_token)
    subject = 'DoomCart Verify Email'
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, (email,) , auth_password = settings.EMAIL_HOST_PASSWORD )


class TokenView(View):
    def get(self, request, token):
        try:
            profile = UserProfile.objects.get(auth_token=token)
        except UserProfile.DoesNotExist :
            messages.warning(request,'This url is false ! Please register again.')
            messages.warning(request,'If already regestered ! generate new Verification link')

            return redirect('generate')
        else :
            profile.is_verified = True
            profile.save()
            messages.success(request, 'Your mail is verified Successfully, Please login')
            return redirect('login')
            

def IsProfileVerified(request):
    return UserProfile.objects.filter(user = request.user).first()


def NotVerified(request):
    messages.warning(request, 'please check your email and verify your account')
    return render(request,'email_varification.html')
        

def Generate(request):
    if request.method == 'POST':
        # if request.user.is_authenticated:
                
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email = email).first()
            if user:
                profile = UserProfile.objects.filter(user=user).first()
                profile.auth_token = str(uuid.uuid4())
                profile.save()
                verifyEmail(user,email)
                return NotVerified(request)
            
            messages.warning(request,'Enter a valid email address')
            return redirect('generate')
        return redirect('login')
    form = ForgotPasswordForm()
    return render(request,'generate.html',{'form':form})
        