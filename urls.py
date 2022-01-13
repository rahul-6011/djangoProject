
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import include, url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('accounts.urls')),
    path('',include('personal.urls')),
    path('',include('books.urls')),
    path('',include('merchant.urls')),
    path('',include('deliveryagent.urls')),
    path('',include('complaint.urls')),
]