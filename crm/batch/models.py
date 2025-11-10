from django.db import models

from students.models import BaseClass

# Create your models here.

class Batch(BaseClass):

    name=models.CharField(max_length=25)

    code=models.CharField(max_length=35)

    course= models.ForeignKey('course.Course',on_delete=models.CASCADE)

    trainer= models.ManyToManyField('trainer.Trainer')

    start_date=models.DateField()

    end_date=models.DateField()



    class meta:

        verbose_name='Batches'

        verbose_name_plural='Batches'

    def __str__(self):
        return self.name    

