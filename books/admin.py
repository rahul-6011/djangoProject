from django.contrib import admin
from .models import Book,OrderItem,Order,Payment, Wishlist, Review

# Register your models here.

admin.site.register(Book)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Wishlist)
admin.site.register(Review)