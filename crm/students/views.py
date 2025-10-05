from django.shortcuts import render, redirect
from django.views import View

from .forms import AddStudentForm ,CourseChoices,BatchChoices,TrainerChoices
from .models import Students

from crm.utils import generate_admission_number

# to implement or

from django.db.models import Q
# Create your views here.




class DashBoardView(View):

    def get(self,request,*args,**kwargs):

        data = {'title':"Dashboard"}

        return render(request,'students/dashboard.html', context=data)
    
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

            students=students.filter(course=course)

        elif batch:   

            students= students.filter(batch=batch)

        elif trainer:
                
            students= students.filter(trainer=trainer)

            

                                     
                                                                            #   to show query and chnge in list 

        data ={"title" : "Students List","students":students,
               'course_choices':CourseChoices,
               'query':query,
               'batch_choices':BatchChoices,
               'trainer_choices':TrainerChoices,
               'course':course,
               'batch':batch,'trainer':trainer}

        return render(request,'students/students_list.html', context=data)
    
class StudentDetailsView(View):

    def get(self,request,*args,**kwargs):


        uuid  = kwargs.get("uuid")

        student = Students.objects.get(uuid=uuid)     #id in space of uuid before

        data = {'title':"Student Details" , 'student': student }

        return render(request,"students/student_details.html",data)


#   for hard delete

# class StudentDeleteView(View):

#     def get(self,request,*args,**kwargs):

#         uuid = kwargs.get('uuid')

#         student = Students.objects.get(uuid=uuid)

#         student.delete()

#         return redirect('students-list')


class AddStudentView(View):

    form_class = AddStudentForm

    def get(self,request,*args,**kwargs):

        form  = self.form_class()

        data = {"form":form,'title':"Add Student"}

        return render(request,'students/add-student.html',context = data)
    
    def post(self,request,*args,**kwargs):

        form =self.form_class(request.POST,request.FILES)

        if form.is_valid():

            student=form.save(commit=False)

            adm_num = generate_admission_number()

            student.adm_num= adm_num

            student.save()

    

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

class EditStudentView(View):
     
     form_class = AddStudentForm

     def get(self,request,*args,**kwargs):
         
         uuid = kwargs.get('uuid')

         student = Students.objects.get(uuid=uuid)

         form = self.form_class(instance = student)

         data = {'form' : form ,'title':"Edit Student"}

         
         return render(request,"students/edit-student.html",data)
    
     def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')
    
        student = Students.objects.get(uuid=uuid)

        form =self.form_class(request.POST,request.FILES,instance = student)
                #    there is a clean method for validation need to override
        if form.is_valid():

            form.save()

            return redirect("students-list")

        data = {'form':form}

        return render(request,"students/edit-student.html",data)
     

# soft Delete

class StudentDeleteView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        student = Students.objects.get(uuid=uuid)

        student.active_status=False

        student.save()

        return redirect('students-list')
