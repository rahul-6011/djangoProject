from django.shortcuts import render,redirect,get_object_or_404
from books.models import Book,OrderItem,Order
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage


# Create your views here.

def addBook(request):
    if request.method == "POST":
        name = request.POST["name"] 
        author = request.POST["author"]
        cost = request.POST["cost"]

        if float(cost) <= 0:
            messages.info(request, "Enter a valid cost value ")
            return redirect("home") 
        
        else:
            uploaded_file = request.FILES["img"]
            fs = FileSystemStorage()
            img = fs.save(uploaded_file.name,uploaded_file)
            book = Book()
            if Book.objects.filter(name = name, author = author, cost= cost, merchant = request.user).exists():
                messages.info(request,"Book exists")
                return redirect("home") 
            else:
                book = Book.objects.create(name = name, author = author, cost= cost, img = img, merchant = request.user)
                book.save()
                messages.info(request,"Book Uploaded")
                return redirect("home") 
    else:
        messages.info(request,"No action")
        return redirect("home")

def book_reqm(request):

    books = Book.objects.filter(merchant=request.user)
    order_items = OrderItem.objects.filter(item__in=books, ordered=True, mer=False)  

    if order_items:
        return render(request,'book_reqm.html',{'order_items':order_items})
    else:
        return render(request,'book_reqm.html')


def accpetm(request,id):
    order = OrderItem.objects.get(id = id)
    order.mer = True
    order.save()
    messages.success(request,"Order Item Accepted")
    return redirect('book_reqm')

def prev_orders(request):
    books = Book.objects.filter(merchant=request.user)
    prorders = OrderItem.objects.filter(mer=True, ordered=True, item__in=books)

    if prorders:
        return render(request,'prvorders.html',{'prorders':prorders})
    else:
        return render(request,'prvorders.html')