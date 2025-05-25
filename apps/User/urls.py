from django.urls import path
from .views import UserRegisterView, UserDetailView, UserProfileView ,AllUserProfileView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('userdetail/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('userprofile/', AllUserProfileView.as_view(), name='all-user-profile'),
    path('userprofile/<int:id>/', UserProfileView.as_view(), name='user-profile'),
    
]
