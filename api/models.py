from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import date
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('the Email field must be required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=20,blank=True,null=True )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.CharField(default=True)
    is_staff = models.BooleanField(default=True)
    location = models.CharField(max_length=10,blank=True)
    native_name = models.CharField(max_length=10)
    birth_date = models.DateField(null=True, blank = True)
    phone_no=models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='profile_pics',blank=True,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Postt(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # If User is deleted, delete their Profile too
    username = models.CharField(max_length=20, blank=True,null=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=400, blank=True)
    location = models.CharField(max_length=100, blank= True)
    birth_date = models.DateField(null=True, blank = True)
    profile_picture = models.ImageField(upload_to='profile_pics',blank=True,null=True)

    def __str__(self):
        return f"{self.user.username}'s Postt"
    

