from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Complaint(models.Model):
    subject = models.CharField(max_length = 150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, default = None)
    complaint = models.TextField()

    def __str__(self):
        return self.subject + ' by ' + self.user.username
