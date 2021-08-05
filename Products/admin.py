from django.contrib import admin
from .models import Cart,OrderPlaced,Product
# Register your models here.
admin.site.register(OrderPlaced)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['productName','category','id']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['customer','id','product']