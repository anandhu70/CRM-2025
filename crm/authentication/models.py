# for different roles 

from django.db import models

from django.contrib.auth.models import AbstractUser

# for otp 

from students.models import BaseClass

# Create your models here.
# need all the feilds   use inheritance
# 
class RoleChoices(models.TextChoices):

    ADMIN='Admin','Admin'

    STUDENT='Student','Student' 

    TRAINER='Trainer','Trainer'

    Sales='Sales','Sales'

    ACADEMIC_COUNCELLOR='Academic_councellor','Academic_councellor'

class Profile(AbstractUser):

    role=models.CharField(max_length=20,choices=RoleChoices.choices)

# meta to avoid s inthe admin
    class Meta:

        verbose_name='Profiles'

        verbose_name_plural='Profiles'

    def __str__(self):
        return self.username    


# need a model to fetch otp and varify

class OTP(BaseClass):

    profile= models.OneToOneField('Profile',on_delete=models.CASCADE)

    email_otp=models.CharField(max_length=4,null=True,blank=True)

    phone_otp= models.CharField(max_length=4,null=True,blank=True)

    # for avoiding direct otp page loading

    otp_verified= models.BooleanField(default=False)

    class Meta:

        verbose_name= 'OTPs'

        verbose_name_plural= 'OTPs'

    def __str__(self):
        return f'{self.Profile.username} OTPs'    

