from django.urls import path,include
from django.conf.urls import url
from . import views


urlpatterns = [
    path('personal',views.personal,name = 'personal'),
    path('password',views.password,name = 'password'),
    path('old_orders',views.old_orders, name = "old_orders"),
    path('retrn/<int:id>',views.retrn,name = 'retrn'),
    path('my_books',views.my_books, name = "my_books"),
]   