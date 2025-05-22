from django.urls import path
from .views import VerifyOtpView


urlpatterns = [
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp')
]
