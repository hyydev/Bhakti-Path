from django.urls import path 
from .views import PaymentInitiateView,RazorpayWebhookView

urlpatterns = [
    path("initiate/", PaymentInitiateView.as_view(),name = "payment-intiate"),
    path("webhook/", RazorpayWebhookView.as_view(),name = "payment-webhook"),
    
]