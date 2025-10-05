from django.db import models

import uuid

# Create your models here.

# for soft delete and keep log 

class BaseClass(models.Model):
                                       #to generatebrandomly
    uuid=models.UUIDField(unique=True,default=uuid.uuid4)

    active_status=models.BooleanField(default=True)
                                     #id created at once
    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    class Meta:

        abstract=True



class EducationChoices(models.TextChoices):

    SSLC = "SSLC" ,'SSLC'

    PLUS_TWO = "PLUS_TWO", "PLUSTWO"

    DIPLOMA=  "DIPLOMA" , "DIPLOMA"

    DEGREE = " DEGREE" , " DEGREE"

    POST_GRADUATE ="POST_GRADUATE" , "POST GRADUATE"


class DistrictChoices(models.TextChoices):

    THIRUVANANTHAPURAM = " THIRUVANANTHAPURAM" , " THIRUVANANTHAPURAM"

    KOLLAM = "KOLLAM" , "KOLLAM"
 
    PATHANAMTHITTA ="PATHANAMTHITTA" , "PATHANAMTHITTA"

    ALAPPUZHA = "ALAPPUZHA","ALAPPUZHA"
 
    KOTTAYAM ="KOTTAYAM" , "KOTTAYAM"

    IDUKKI =  "IDUKKI " , "IDUKKI "
 
    ERNAKULAM ="ERNAKULAM","ERNAKULAM"

    THRISSUR ="THRISSUR","THRISSUR"
 
    PALAKKAD ="PALAKKAD","PALAKKAD"

    MALAPPURAM ="MALAPPURAM" , "MALAPPURAM"

    KOZHIKODE = "KOZHIKODE","KOZHIKODE"

    WAYANAD ="WAYANAD","WAYANAD"

    KANNUR ="KANNUR","KANNUR"
 
    KASARAGOD ="KASARAGOD" ,"KASARAGOD"


class CourseChoices(models.TextChoices):

    PYDJANGO = "Py Django" , "Py Django"

    MEARN = "MEARN","MEARN"

    DS = "Data Science" ,"Data Science"


class BatchChoices(models.TextChoices):
    BATCH_1 ="BATCH_1","BATCH_1"
    BATCH_2 ="BATCH_2", "BATCH_2"
    BATCH_3 ="BATCH_3","BATCH_3"
    BATCH_4 = "BATCH_4" , "BATCH_4"
class TrainerChoices(models.TextChoices):

    JOHN ="john" , "John"

    JAMES ="James","James"

    ALEX = "Alex" , "Alex"


class Students(BaseClass):

    first_name = models.CharField(max_length=25)

    last_name = models.CharField(max_length=25)

    adm_num = models.CharField(max_length=8)

    email = models.EmailField(unique=True)

    contact_num = models.CharField(max_length=13,unique=True)

    photo = models.ImageField(upload_to='students-photos')

    dob = models.DateField()

    education = models.CharField(max_length=15,choices=EducationChoices.choices)

    address = models.CharField(max_length=50)

    place = models.CharField(max_length=15)

    district = models.CharField( max_length=20, choices=DistrictChoices.choices)
    
    pincode = models.CharField(max_length=6)

    course = models.CharField(max_length=20, choices=CourseChoices.choices)

    batch = models.CharField(max_length=10,choices=BatchChoices.choices)

    trainer = models.CharField(max_length=15,choices=TrainerChoices.choices)

    join_date = models.DateField(auto_now_add=True) # if use auto_now -- then it will upate every chainge or update the field

    def __str__(self):

        return f"{self.first_name}-{self.last_name}-{self.adm_num} "


    class Meta :

        verbose_name = "Students"

        verbose_name_plural ='Students'

'''
    first_name
    last_name
    adm_num
    email
    contact_num
    photo
    dob
    education
    address
    place
    district
    course
    batch
    trainer
    join_date
    
    '''