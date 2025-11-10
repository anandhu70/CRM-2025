from django.urls import path
from . import views

urlpatterns=[
    path('course-list/',views.CourseListView.as_view(),name='course-list'),
    path('add-course/',views.AddCourseView.as_view(),name='add-course'),

    path('edit-course/<str:uuid>/',views.EditCourseView.as_view(),name='edit-course'),

    path('delete-course/<str:uuid>/',views.CourseDeleteView.as_view(),name='delete-course'),

    path('course-details/<str:uuid>/',views.CourseDetailsView.as_view(),name='course-details'),



    
]