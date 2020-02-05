from django.db import models
from django.conf import settings
from django.shortcuts import reverse


CATEGORY_CHOICE=(
    ('P','pizza'),
    ('B','burger'),
    ('R','rice'),
    ('S', 'salad'),
    ('O','others')
)
# Create your models here.
class Product(models.Model):
    name =models.CharField(max_length=50)
    price=models.FloatField()
    description=models.TextField()
    category=models.CharField(choices=CATEGORY_CHOICE,max_length=2)
    image=models.ImageField()
    slug=models.SlugField()


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product",kwargs={
            'slug':self.slug
        })
    def get_add_to_cart(self):
        return reverse("add-to-cart", kwargs={
          'slug':self.slug  
        })
    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
          'slug':self.slug  
        })

class OrderProduct(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    ordered=models.BooleanField(default=False)

    


    def __str__(self):
        return f"{self.quantity} of {self.item.name}"
    
    def get_total_item_price(self):
        return self.quantity * self.item.price

    
        


class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products=models.ManyToManyField(OrderProduct)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ref_code=models.CharField(max_length=20)
    ordered=models.BooleanField(default=False)
    shipping_address=models.ForeignKey('ShippingAddress',on_delete=models.SET_NULL, blank=True, null=True)
    payment=models.ForeignKey('Payment',on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered=models.BooleanField(default=False)
    received=models.BooleanField(default=False)
    delivery_msg=models.TextField( blank=True, null=True)
    def __str__(self):
        return self.user.username


    def get_total(self):
        total=0
        for order_item in self.products.all():
            total += order_item.get_total_item_price()
        return total 

class ShippingAddress(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    apartment_no=models.CharField(max_length=4)
    street_name=models.CharField(max_length=50)
    area=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username

class Payment(models.Model):
    stripe_charge_id=models.CharField(max_length=60)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount=models.FloatField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



