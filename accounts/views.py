from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.

def index(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        acc_type = request.POST['acc_type']

        user = auth.authenticate(username = email, password = password)
        
        if user is not None:
            user1 = User.objects.get(username=email)
            if user1.last_name == acc_type:
                auth.login(request,user)
                if user1.last_name == 'customer':
                    return redirect('home')
                elif user1.last_name == 'merchant':
                    return render(request, 'home_m.html')
                else:
                    return redirect('home_d')
            else:
                messages.info(request,'*Invalid Credentials')
                return redirect('index')

        
        else:
            messages.info(request,'*Invalid Credentials')
            return redirect('index')

    else:
        return render(request, 'index.html')
    

def register(request):

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        acc_type = request.POST['acc_type']

        if(password1 == password2):
            if User.objects.filter(username=email).exists():
                print('Email taken')
                messages.info(request,'*Email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name = name,last_name = acc_type, password = password1 , username = email)
                user.save()
                print('user created')
                return redirect('index')
        else:
            messages.info(request,'*Passwords do not match')
            return redirect('register')
    else:
        return render(request,'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')