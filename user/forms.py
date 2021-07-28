from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField,PasswordChangeForm , PasswordResetForm ,SetPasswordForm
from django.contrib.auth.models import User
from .models import Customer


class RegisterationForm(UserCreationForm):
    password1 = forms.CharField(
        label = 'Password',
        required = True,
        widget = forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(
        label = 'Confirm password', 
        required = True ,
        widget = forms.PasswordInput(attrs={'class':'form-control'})) 
    email = forms.CharField(
        label = 'Email' ,
        required = True ,
        widget = forms.EmailInput(attrs={'class':'form-control'}))   
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']
        widgets = { 'username':forms.TextInput(attrs={'class':'form-control'})}
        

class LoginForm(AuthenticationForm):
    """LoginForm definition."""
    username = UsernameField(
        widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password = forms.CharField(
        label = 'Password', 
        required = True ,
        widget=forms.PasswordInput(attrs={'class':'form-control'}))



class changePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label = 'Old Password' , 
        required = True ,
        widget=forms.PasswordInput(attrs={'class':'form-control','autofocus':True}))
    new_password1 = forms.CharField(
        label = 'New Password',
        required = True ,
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(
        label = 'Confirm Password',
        required = True ,
        widget=forms.PasswordInput(attrs={'class':'form-control'}))



class ForgotPasswordForm(PasswordResetForm):
    email = forms.CharField(
        label = 'Email',
        required = True ,
        widget=forms.EmailInput(attrs={'class':'form-control','autofocus':True}))


class NewPasswordConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label = 'New Password',
        required = True ,
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(
        label = 'Confirm Password',
        required = True ,
        widget=forms.PasswordInput(attrs={'class':'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'loaclity','city','state','zipCode','phoneNumber']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'loaclity': forms.TextInput(attrs={'class':'form-control'}),
            'city' : forms.TextInput(attrs={'class':'form-control'}),
            'state' : forms.Select(attrs={'class':'form-control'}),
            'zipCode': forms.NumberInput(attrs={'class':'form-control'}),
            'phoneNumber' : forms.NumberInput(attrs={'class':'form-control'})
        }
