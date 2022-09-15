from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class UserPassword(models.Model):
    cust=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    pwd=models.CharField(max_length=50)