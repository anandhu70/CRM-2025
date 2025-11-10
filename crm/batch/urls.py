from django.urls import path
from . import views


urlpatterns=[path('add-batch/',views.AddBatchView.as_view(),name='add-batch')
             
             ]
