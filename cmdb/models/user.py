from hashlib import md5

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=16)
    salt = models.CharField(max_length=16)
    addr = models.CharField(max_length=50, null=True)
    loc_lng = models.DecimalField(max_digits=9, decimal_places=5, null=True)
    loc_lat = models.DecimalField(max_digits=9, decimal_places=5, null=True)
    phone = models.CharField(max_length=11)

    def check_password(self, password):
        """Check if the given password matches"""
        return md5((password + ':' + self.salt).encode('utf-8')).hexdigest()[8:-8] == self.password

    def set_password(self, password):
        """Set the current password to the given one"""
        self.password = md5((password + ':' + self.salt).encode('utf-8')).hexdigest()[8:-8]
