from django.urls import path,include
from django.conf.urls import url
from . import views


urlpatterns = [
    path('complaint', views.complaint, name = 'complaint'),
]
