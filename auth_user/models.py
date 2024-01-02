from django.db import models
from .constants import GENDER_TYPE
from django.contrib.auth.models import User


class UserLibraryAccount(models.Model):
    user = models.OneToOneField(User, related_name='account',on_delete=models.CASCADE)
    account_no = models.IntegerField(unique=True)
    birth_date = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=100, choices=GENDER_TYPE)
    profile_picture = models.ImageField(upload_to='auth_user/media/uploads/', blank = True, null = True)
    initial_deposite_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return str(self.account_no)




class  UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address',on_delete=models.CASCADE)
    postal_code = models.IntegerField()
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)