from django.db import models


# Create your models here.
class user(models.Model):
    userId = models.AutoField(primary_key=True)

    username = models.CharField(max_length=20)

    password = models.CharField(max_length=16)

    salt = models.CharField(max_length=16)

    phone = models.CharField(max_length=11)
