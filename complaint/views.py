from django.shortcuts import render,redirect 
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Complaint

# Create your views here.

@login_required
def complaint(request):

    if request.method == 'POST':
        subject = request.POST['subject']
        complaint = request.POST['complaint']

        comp = Complaint.objects.create(user=request.user, subject=subject, complaint=complaint)

        messages.info(request, "Complaint sent")


    return render(request, "complaint.html")
