from django.shortcuts import render,redirect,get_object_or_404
from books.models import Book,OrderItem,Order
from django.contrib import messages
from django.conf import settings


# Create your views here.

def home_d(request):

    order_items = OrderItem.objects.filter(ordered=True,mer=True, delivered = False)

    if order_items:
        return render(request,'home_d.html',{'order_items':order_items})
    else:
        return render(request,'home_d.html')

def accpetd(request,id):
    order = OrderItem.objects.get(id = id)
    order.dely = True
    order.dagent = request.user
    order.save()
    messages.success(request,"Order Accepted")
    return redirect('home_d')


def delivd(request,id):
    order = OrderItem.objects.get(id = id)
    order.delivered = True
    order.dagent = None
    order.save()
    messages.success(request,"Order Delivered")
    return redirect('home_d')


def retrn_reqd(request):

    order_items = OrderItem.objects.filter(ordered=True,return_started = True,returned = False)
    
    if order_items:
        return render(request,'retrn_reqd.html',{'order_items':order_items})
    else:
        return render(request,'retrn_reqd.html')

def accptd_rtn(request,id):
    order = OrderItem.objects.get(id = id)
    order.return_accepted = True
    order.dagent = request.user
    order.save()
    messages.success(request,"Order Accepted")
    return redirect('retrn_reqd')

def delivd_rtn(request,id):
    order = OrderItem.objects.get(id = id)
    order.returned = True
    order.dagent = None
    order.save()
    messages.success(request,"Return Taken")
    return redirect('retrn_reqd')
