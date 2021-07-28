from django.contrib import admin
from .models import Cart,Customer,OrderPlaced,Product
# Register your models here.
admin.site.register(Customer)
admin.site.register(OrderPlaced)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['productName','category','id']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['customer','id','product']