from django.urls import path 
from .views import PaymentInitiateView,RazorpayWebhookView, RazorpayPaymentVerifyView

urlpatterns = [
    path("initiate/", PaymentInitiateView.as_view(),name = "payment-intiate"),
    path('payments/verify/', RazorpayPaymentVerifyView.as_view(), name='payment-verify'),
    path("webhook/", RazorpayWebhookView.as_view(),name = "payment-webhook"),
    
]