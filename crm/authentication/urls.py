from django.urls import path

from . import views

urlpatterns=[

    path('',views.LoginView.as_view(),name='login'),

    path('logout/',views.LogoutView.as_view(),name='logout'),

    path('otp/',views.OtpView.as_view(),name='otp'),

    path('change_password/',views.ChangePasswordView.as_view(),name='change-password')


]