from django.shortcuts import render, redirect
from django.views import View

from .forms import AddStudentForm ,CourseChoices,BatchChoices,TrainerChoices
from .models import Students

from crm.utils import generate_admission_number,generate_password,sent_mail

# to implement or

from django.db.models import Q

# for making it model 

from trainer.models import Trainer

from batch.models import Batch

from course.models import Course
# Create your views here.

# import profiles for profile creation

from authentication.models import Profile,OTP


# for considering creation and profiles as one so one fail both get dltd

from django.db import transaction

# for mail 

from  decouple import config

# for threading (parallel)


import threading

# login permissions 

# from django.contrib.auth.decorators import login_required

# to apply decorators for methods

from django.utils.decorators import method_decorator

from authentication.permissions import permited_users

#(no direct redirect by typing dasboard)                                  
                                         #first it goes to dispatch so commonly implement 

                                           #nam given in url patrn
# @method_decorator(login_required(login_url='login'),name='dispatch')

class DashBoardView(View):
    
    def get(self,request,*args,**kwargs):

        

        data = {'title':"Dashboard"}



        return render(request,'students/dashboard.html', context=data)
    

@method_decorator(permited_users(['Admin','Sales']),name='dispatch')
    
class StudentView(View):

    def get(self,request,*args,**kwargs):

        # for search  and dropdown box and its inner shown

        query=request.GET.get('query')

        course=request.GET.get('course')

        batch=request.GET.get('batch')

        trainer=request.GET.get('trainer')


 #.all for showing
        students=Students.objects.filter(active_status=True)

        if query:

            # implement  search  in every string in models  and import  Q 

            students=students.filter (




                                        Q(first_name__icontains=query)|

                                        Q(last_name__icontains=query)|

                                        Q(adm_num__icontains=query)|

                                        Q(email__icontains=query)|

                                        Q(contact_num__icontains=query)|

                                        Q(education__icontains=query)|

                                        Q(address__icontains=query)|

                                        Q(place__icontains=query)|

                                        Q(district__icontains=query)|

                                        Q(course__icontains=query)|

                                        Q(batch__icontains=query)|

                                        Q(trainer__icontains=query)|

                                        Q(pincode__icontains=query)  )
            

        elif course:

            students=students.filter(course__name=course)
            # students=students.filter(course=course) object


        elif batch:   

            students= students.filter(batch__name=batch)

        elif trainer:
                
            students= students.filter(trainer__name=trainer)

            

                                     
                                                                            #   to show query and chnge in list 

        data ={"title" : "Students List","students":students,
            #    'course_choices':CourseChoices   for models convert,
               
               'course_choices':Course.objects.all(),
               'query':query,
               'batch_choices':Batch.objects.all(),
               'trainer_choices':Trainer.objects.all(),
               'course':course,
               'batch':batch,'trainer':trainer}

        return render(request,'students/students_list.html', context=data)
    
@method_decorator(permited_users(['Admin','Sales']),name='dispatch')
    
class StudentDetailsView(View):

    def get(self,request,*args,**kwargs):


        uuid  = kwargs.get("uuid")

        student = Students.objects.get(uuid=uuid)     #id in space of uuid before

        data = {'title':"Student Details" , 'student': student }

        return render(request,"students/student_details.html",context=data)


#   for hard delete

# class StudentDeleteView(View):

#     def get(self,request,*args,**kwargs):

#         uuid = kwargs.get('uuid')

#         student = Students.objects.get(uuid=uuid)

#         student.delete()

#         return redirect('students-list')

@method_decorator(permited_users(['Admin','Sales']),name='dispatch')

class AddStudentView(View):

    form_class = AddStudentForm

    def get(self,request,*args,**kwargs):

        form  = self.form_class()

        # print(request.user.meta.get_feilds())---reverse lookup denotes

        data = {"form":form,'title':"Add Student"}

        return render(request,'students/add-student.html',context = data)
    
    def post(self,request,*args,**kwargs):

        form =self.form_class(request.POST,request.FILES)

        if form.is_valid():

            # using transaction for profile and studen creation as one 

            with transaction.atomic():

                student=form.save(commit=False)

            # to create random adis no

                adm_num = generate_admission_number()

                student.adm_num= adm_num

            # to create profile

                email=form.cleaned_data.get('email')

                password=generate_password()

                print(password)
                                    # orm query to create user 

                profile=Profile.objects.create_user(username=email,password=password,role='Student')

                OTP.objects.create(profile=profile)

            # to show profile

                student.profile=profile

                student.save()

                recepient=student.email

                template='email/credentials.html'

                site_link= config('SITE_LINK')

                context={'username':student.email,'password':password,'name':f'{student.first_name} {student.last_name}','site_link':site_link}

                title='login credetials'
                                    # name of func if para use args
                thread=threading.Thread(target=sent_mail,args=(recepient,template,context,title))

                thread.start()

                # sent_mail(recepient,template,context,title)   for normal email snt time consuming series

                

       

                return redirect("students-list")
        
        data = {'form':form}
        
        return render(request,'students/add-student.html',context = data)

        # post_data = request.POST

        # first_name = post_data.get("first_name")

        # last_name = post_data.get("last_name")

        # adm_num  = post_data.get('adm_num')

        # email = post_data.get('email')

        # contact_num =post_data.get('contact_num')

        # photo =request.FILES.get('photo')

        # dob = post_data.get('dob')

        # education = post_data.get("education")

        # address = post_data.get("address")

        # place = post_data.get("place")

        # course = post_data.get("course")

        # district = post_data.get("district")

        # pincode = post_data.get("pincode")

        # batch = post_data.get("batch")

        # trainer = post_data.get("trainer")

        # place = post_data.get("place")
      
        # student = Students.objects.create(first_name =  first_name ,last_name = last_name,adm_num  = adm_num ,course=course,  email = email , contact_num = contact_num, photo = photo,  dob = dob , education = education,address  = address, place = place , district =  district, pincode = pincode ,batch = batch ,trainer = trainer )
@method_decorator(permited_users(['Admin','Sales']),name='dispatch')

class EditStudentView(View):
     
     form_class = AddStudentForm

     def get(self,request,*args,**kwargs):
         
         uuid = kwargs.get('uuid')

         student = Students.objects.get(uuid=uuid)

         form = self.form_class(instance = student)

         data = {'form' : form ,'title':"Edit Student"}

         
         return render(request,"students/edit-student.html",context=data)
    
     def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')
    
        student = Students.objects.get(uuid=uuid)

        form =self.form_class(request.POST,request.FILES,instance = student)
                #    there is a clean method for validation need to override
        if form.is_valid():

            form.save()

            return redirect("students-list")

        data = {'form':form}

        return render(request,"students/edit-student.html",context=data)
     

# soft Delete

@method_decorator(permited_users(['Admin','Sales']),name='dispatch')


class StudentDeleteView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        student = Students.objects.get(uuid=uuid)

        student.active_status=False

        student.save()

        return redirect('students-list')
