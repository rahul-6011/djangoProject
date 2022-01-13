from django.urls import path,include
from django.conf.urls import url
from . import views


urlpatterns = [
    path('add_book',views.addBook,name = "add_book"),
    path('prev_orders',views.prev_orders,name = "prev_orders"),
    path('book_reqm',views.book_reqm,name = "book_reqm"),
    path('accpetm/<int:id>',views.accpetm,name = "accpetm"),    
]