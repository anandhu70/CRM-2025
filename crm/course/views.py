from django.shortcuts import render,redirect

from django.views import View

from .models import Course
from django.db.models import Q

from django.utils.decorators import method_decorator

from authentication.permissions import permited_users

from .forms import AddCourseForm

# Create your views here. for permission
@method_decorator(permited_users(['Admin','Sales']),name='dispatch')

class CourseListView(View):

    def get (self,request,*args,**kwargs):

        query=request.GET.get('query')


        courses=Course.objects.filter(active_status=True)

        if query:

            courses=courses.filter(Q(code__icontains=query)|
                                     Q(name__icontains=query)|
                                     Q(mode__icontains=query)
                                       
                                     
                                     
                                     
                                     )
                                
                                  

        data={'courses':courses,'query':query}

        return render(request,'course/course-list.html',context=data)
    
@method_decorator(permited_users(['Admin','Sales']),name='dispatch')
    
class AddCourseView(View):

    form_class = AddCourseForm

    def get(self,request,*args,**kwargs):

        form  = self.form_class()

        # print(request.user.meta.get_feilds())---reverse lookup denotes

        data = {"form":form,'title':"Add Course"}

        return render(request,'course/add-course.html',context = data)
    
    def post(self,request,*args,**kwargs):

        form =self.form_class(request.POST)

        if form.is_valid():

          form.save() 

          return redirect('course-list')  

        
        data = {'form':form}
        
        return render(request,'course/add-course.html',context = data)    

@method_decorator(permited_users(['Admin','Sales']),name='dispatch')

class EditCourseView(View):
     
     form_class = AddCourseForm

     def get(self,request,*args,**kwargs):
         
         uuid = kwargs.get('uuid')

         course = Course.objects.get(uuid=uuid)

         form = self.form_class(instance = course)

         data = {'form' : form ,'title':"Edit Course"}

         
         return render(request,"Course/edit-Course.html",context=data)
    
     def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')
    
        course = Course.objects.get(uuid=uuid)

        form =self.form_class(request.POST,instance = course)
                #    there is a clean method for validation need to override
        if form.is_valid():

            form.save()

            return redirect("course-list")

        data = {'form':form}

        return render(request,"course/edit-course.html",context=data)
     

@method_decorator(permited_users(['Admin','Sales']),name='dispatch')

class CourseDeleteView(View):

     def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        course = Course.objects.get(uuid=uuid)

        course.active_status=False

        course.save()

        return redirect('course-list')
     
@method_decorator(permited_users(['Admin','Sales']),name='dispatch')
    
class CourseDetailsView(View):

    def get(self,request,*args,**kwargs):


        uuid  = kwargs.get("uuid")

        course = Course.objects.get(uuid=uuid)     #id in space of uuid before

        data = {'title':"Course Details" , 'course': course }

        return render(request,"course/course-details.html",context=data)

