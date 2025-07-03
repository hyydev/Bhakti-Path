from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import VerifyOtpView,UserLoginView,UserLogoutView,ForgetPasswordView,VerifyResetOtpView,ResetPasswordView



urlpatterns = [
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('verify-reset-otp/', VerifyResetOtpView.as_view(), name='verify_reset_otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    
]
