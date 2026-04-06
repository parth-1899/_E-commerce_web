from django import forms
from django.contrib.auth.models import User
from .models import SellerProfile, Product


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Create a password'}))
    role = forms.ChoiceField(choices=[('buyer', 'Buyer'), ('seller', 'Seller')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email address'}),
        }


class SellerForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['business_doc', 'isi_certificate']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Product name'}),
            'price': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your product...', 'rows': 4}),
        }
