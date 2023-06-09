from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserOTP(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    time_st = models.DateTimeField(auto_now= True)
    otp = models.IntegerField()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank = True, max_length = 100)
    address_line_2 = models.CharField(blank = True, max_length = 100)
    profile_picture = models.ImageField(blank = True, upload_to='userprofile' )
    email = models.CharField(blank = True, max_length=100)
    phone = models.CharField(max_length=10,null=True,blank = True)
    city = models.CharField(blank = True, max_length = 20)
    state = models.CharField(blank = True, max_length = 20)
    country = models.CharField(blank = True, max_length = 20)
    
    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line_1}{self.address_line_2}'
    

