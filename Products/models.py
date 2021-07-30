from django.db import models
from django.contrib.auth.models import User
from user.models import Customer
from cloudinary.models import CloudinaryField

# Create your models here.




CATEGORY_CHOICES =(
    ('mobile','mobile'),
    ('laptop','laptop'),
    ('shirt','shirt'),
    ('jeans','jeans')
)


class Product(models.Model):
    productName = models.CharField(max_length=200)
    discription = models.TextField()
    brand = models.CharField(max_length=20)
    category = models.CharField(max_length=20 , choices=CATEGORY_CHOICES)
    productImage = CloudinaryField('productImage')
    sellingPrice = models.FloatField()
    discountPrice = models.FloatField()

    def __str__(self):
        return self.productName


class Cart(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.customer.username + "  " + self.product.productName

    @property
    def TotalCost(self):
        return self.quantity * self.product.discountPrice



ORDER_CHOICES =(
    ('Panding', 'Panding'),
    ('Accepted','Accepted'),
    ('On The Way','On The Way'),
    ('Cancelled','Cancelled'),
    ('Packed','Packed'),
    ('Delivered','Delivered')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    orderDate = models.DateField( auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_CHOICES,default='Pending')


    def __str__(self):
        return self.customer.name + ' ' + self.product.productName
