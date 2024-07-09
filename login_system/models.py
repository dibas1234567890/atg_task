from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as AbstractUserManager
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

class CustomUserManager(AbstractUserManager):
    def get_all_patients(self):
        return self.get_queryset().filter(user_type = 'patient')
    def get_all_doctors(self):
        return self.get_queryset().filter(user_type = 'doctor')
    def get_by_user_type(self, user_type):
        return self.get_queryset().get(user_type = user_type)

class CustomerUserProfile(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(("email address"),unique=True)
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100) 
    address_line1 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(  max_length=10)
    user_type = models.CharField( choices= {'patient':'patient', 'doctor':'doctor'} , max_length=10)

    custommanager = CustomUserManager()



        

        

