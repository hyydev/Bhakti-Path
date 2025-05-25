from django.urls import path
from .views import UserRegisterView, UserDetailView, UserProfileView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('userdetail/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('userprofile/<int:id>/', UserProfileView.as_view(), name='user-profile'),
    
]
