from django.db import models

from students.models import BaseClass

# for slection pages(different options) 

import multiselectfield

# Create your models here.

class ModeChoices(models.TextChoices):

    ONLINE= 'Online','Online'

    OFFLINE= 'Offline','Offline'

    HYBRID= 'Hybrid','Hybrid'

class Course(BaseClass):

    name=models.CharField(max_length=25)

    code = models.CharField(max_length=15)

    fee= models.FloatField()

    offer_percent = models.IntegerField()

    mode = multiselectfield.MultiSelectField(max_length=15,choices=ModeChoices.choices)
    @property
    def get_offer_fee(self):

        offer_fee=self.fee - (self.fee*self.offer_percent/100)

    

        return offer_fee



    class meta:

        verbose_name='Courses'

        verbose_name_plural='courses'

    def __str__(self):
        return self.name    
