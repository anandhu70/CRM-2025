from django.urls import path

from . import views

urlpatterns=[

    path('student-payment/',views.StudentPaymentView.as_view(),name='student-payment'),

    path('set-payment/',views.StudentPaymentSetView.as_view(),name='set-payment'),

    path('payment-list/',views.StudentPaymentListView.as_view(),name='payment-list'),

    path('razorpay/',views.RazorPayView.as_view(),name='razorpay'),

    path('razorpay-emi/<str:uuid>/',views.RazorPayView.as_view(),name='razorpay-emi'),


    path('payment-verify/',views.PaymentVerifyView.as_view(),name='payment-verify'),
    path('generate-invoice/',views.GeneratePDFView.as_view(),name='generate-invoice'),

    path('generate-invoice-emi/<str:uuid>/',views.GeneratePDFView.as_view(),name='generate-invoice-emi'),



]