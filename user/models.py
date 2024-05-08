from django.db import models
from django.contrib.auth.models import AbstractUser
from user.manager import UserManager


class UserProfile(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=False)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    objects = UserManager()
    
    # REQUIRED_FIELDS = ['email']
    def __str__(self):
        return self.phone_number
    
    
class UserOtp(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='otp')
    otp = models.CharField(max_length=8, blank=True, null=True)