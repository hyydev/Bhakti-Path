from django.urls import path 
from .views import PaymentInitiateView

urlpatterns = [
    path("initiate/", PaymentInitiateView.as_view(),name = "payment-intiate"),
    
]