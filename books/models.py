from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.db import models

# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length = 100)
    author = models.CharField(max_length = 100)
    img = models.ImageField(upload_to='images')
    cost = models.FloatField()
    merchant = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, default = None)

    def __str__(self):
        return self.name + ' by ' + self.author

       
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, default = None, related_name = 'customer')
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Book, on_delete=models.CASCADE)
    dagent = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True, default = None, related_name = 'delivery_agent')
    quantity = models.IntegerField(default=1)
    delivered = models.BooleanField(default =False)
    mer = models.BooleanField(default =False)
    dely = models.BooleanField(default =False)
    return_started = models.BooleanField(default =False)
    return_accepted = models.BooleanField(default =False)
    returned = models.BooleanField(default =False)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.cost


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default = None)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default =False)

    street_address = models.CharField(max_length = 200, default = None,blank = True,null = True)
    apartment_address = models.CharField(max_length = 200, default = None,blank = True,null = True)
    country = CountryField(multiple = False, default = None,blank = True,null = True)
    zip = models.CharField(max_length = 10, default = None,blank = True,null = True)

    payment = models.ForeignKey('Payment',on_delete = models.SET_NULL,blank = True,null = True)

    def __str__(self):
        return f"Order no.{self.id} - {self.user.username} "

    def get_total_price(self):
        total = 0
        for it in self.items.all():
            total += it.get_total_item_price()
        return total


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank = True,null = True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.user.username} "


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank = True,null = True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.name + " by " + self.user.username
        


class Review(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, default = None)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    descrp = models.TextField()
    
    def __str__(self):
        return "Review of " + self.book.name + " by " + self.customer.username
