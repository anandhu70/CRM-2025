from django.db import models

from students.models import BaseClass

# Create your models here.

class Trainer(BaseClass):

    name=models.CharField(max_length=25)

    class meta:

        verbose_name='Trainer'

        verbose_name_plural='trainer'

    def __str__(self):
        return self.name    
