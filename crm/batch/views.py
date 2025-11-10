from django.shortcuts import render,redirect

from django.views import View

from .models import Batch
from django.db.models import Q

from django.utils.decorators import method_decorator

from authentication.permissions import permited_users

from .forms import AddBatchForm

from crm.utils import get_batch_code,get_end_date

# Create your views here.
@method_decorator(permited_users(['Admin','Sales']),name='dispatch')

# class BatchListView(View):

#     def get (self,request,*args,**kwargs):

#         query=request.GET.get('query')


#         batches=Batch.objects.filter(active_status=True)

#         if query:

#             courses=courses.filter(Q(code__icontains=query)|
#                                      Q(name__icontains=query)|
#                                      Q(trainer__icontains=query)|
#                                      Q(batch__icontains=query)|
#                                      Q(start_date__icontains=query)|
#                                      Q(end_date__icontains=query)



                                       
                                     
                                     
                                     
#                                      )
                                
                                  

#         data={'batches':batches,'query':query}

#         return render(request,'batch/batch-list.html',context=data)
    

@method_decorator(permited_users(['Admin','Sales']),name='dispatch')
    
class AddBatchView(View):

    form_class = AddBatchForm

    def get(self,request,*args,**kwargs):

        form  = self.form_class()

        # print(request.user.meta.get_feilds())---reverse lookup denotes

        data = {"form":form,'title':"Add Batch"}

        return render(request,'batch/add-batch.html',context = data)
    
    def post(self,request,*args,**kwargs):

        form =self.form_class(request.POST)

        if form.is_valid():

          batch=form.save(commit=False)

          start_date= form.cleaned_data.get('start_date') 

          batch_code=get_batch_code(batch.course,start_date)

        #   form.save()

          print(batch_code)

          end_date=get_end_date(start_date)

          print(end_date)

          batch.code=batch_code

          batch.end_date= end_date
          
          batch.save()

          form.save_m2m

          return redirect('course-list')  

        
        data = {'form':form}
        
        return render(request,'batch/add-batch.html',context = data)    

# @method_decorator(permited_users(['Admin','Sales']),name='dispatch')

# class EditBatchView(View):
     
#      form_class = AddBatchForm

#      def get(self,request,*args,**kwargs):
         
#          uuid = kwargs.get('uuid')

#          batch= Batch.objects.get(uuid=uuid)

#          form = self.form_class(instance = batch)

#          data = {'form' : form ,'title':"Edit Batch"}

         
#          return render(request,"Batch/edit-batch.html",context=data)
    
#      def post(self,request,*args,**kwargs):

#         uuid = kwargs.get('uuid')
    
#         batch = Batch.objects.get(uuid=uuid)

#         form =self.form_class(request.POST,instance =batch)
#                 #    there is a clean method for validation need to override
#         if form.is_valid():

#             form.save()

#             return redirect("batch-list")

#         data = {'form':form}

#         return render(request,"batch/edit-batch.html",context=data)
     

# @method_decorator(permited_users(['Admin','Sales']),name='dispatch')

# class BatchDeleteView(View):

#      def get(self,request,*args,**kwargs):

#         uuid = kwargs.get('uuid')

#         batch = Batch.objects.get(uuid=uuid)

#         batch.active_status=False

#         batch.save()

#         return redirect('batch-list')
     
# @method_decorator(permited_users(['Admin','Sales']),name='dispatch')
    
# class BatchDetailsView(View):

#     def get(self,request,*args,**kwargs):


#         uuid  = kwargs.get("uuid")

#         batch = Batch.objects.get(uuid=uuid)     #id in space of uuid before

#         data = {'title':"Batch Details" , 'batch': batch }

#         return render(request,"batch/batch-details.html",context=data)

