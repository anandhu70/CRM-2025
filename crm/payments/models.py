from django.db import models

from students.models import BaseClass

from django.utils import timezone

# Create your models here.

class PaymentOptionChoices(models.TextChoices):

    EMI= 'EMI','EMI'

    ONE_TIME='One Time','One Time'

class EMINumberChoices(models.IntegerChoices):
    
    ZERO=0,'00'

    Two=2,'2'

    THREE=3,'3'    


class Payment(BaseClass):

    student=models.ForeignKey('students.Students',on_delete=models.CASCADE)

    course=models.ForeignKey('course.Course',on_delete=models.CASCADE)

    payment_option=models.CharField(max_length=15,choices=PaymentOptionChoices.choices)

    no_of_emi=models.IntegerField(choices=EMINumberChoices.choices,default=0)

    fee=models.FloatField()

    amount_to_be_paid=models.FloatField()

    full_paid=models.BooleanField(default=False)
    @property
    def  get_due_date(self):

        join_date=self.student.join_date

        due_date=join_date+timezone.timedelta(days=10)

        return due_date
    
    def __str__(self):
        return f'{self.student.first_name}-{self.student.last_name}-{self.course.name}-payment' 
    
    class meta:

        verbose_name='Payments'

        verbose_name_plural='Payments'
    
class InstallmentChoices(models.IntegerChoices):

    ONE = 1,'1'

    TWO = 2,'2'

    THREE = 3,'3'

class EMI(BaseClass):
                                                                     #can give name of choices so both look same can call both
    payment = models.ForeignKey('Payment',on_delete=models.CASCADE,related_name='emi')

    installment_no  = models.IntegerField(choices=InstallmentChoices.choices)

    amount = models.FloatField()

    due_date = models.DateField()

    paid = models.BooleanField(default=False)

    def __str__(self):

        return f'{self.payment.student.first_name}-{self.payment.student.last_name}--{self.payment.course.name}--EMI--{self.installment_no}'
    
    class Meta:

        verbose_name = 'EMIs'

        verbose_name_plural = 'EMIs'  

class PaymentStatusChoices(models.TextChoices):

    SUCCESS='Success','Success'  

    PENDING='Pending','Pending'

    FAILED='Failed','Failed' 

class Transaction(BaseClass):

    payment= models.ForeignKey('Payment',on_delete=models.CASCADE)

    emi=models.ForeignKey('Emi',null=True,on_delete=models.CASCADE)
    
    rzp_order_id=models.SlugField()

    amount=models.FloatField()

    status=models.CharField(max_length=20,choices=PaymentStatusChoices.choices,default=PaymentStatusChoices.PENDING)

    transaction_at=models.DateField(null=True,blank=True)

    rzp_payment_id= models.SlugField(null=True,blank=True)

    rzp_signature=models.TextField(null=True,blank=True)

    def __str__(self):
        return f'{self.payment.student.first_name} {self.payment.student.last_name}{self.rzp_order_id} transaction' 

    class Meta:

        verbose_name='Trnsactions'

        verbose_name_plural='Trnsactions'







    

    



