from django.contrib import admin

# Register your models here.
from .models import *

from django.contrib import admin
from .models import Profile, SellerProfile, Product, Order


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified']
    list_editable = ['is_verified']
    list_filter = ['is_verified']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'seller']
    list_filter = ['seller']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'status', 'ordered_at']
    list_filter = ['status']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
