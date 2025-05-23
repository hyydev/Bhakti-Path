from django.urls import path
from .views import VerifyOtpView,UserLoginView


urlpatterns = [
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),
    path('login/', UserLoginView.as_view(), name='user_login'),

]
