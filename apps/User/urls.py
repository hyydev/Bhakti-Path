from django.urls import path
from .views import UserRegisterView, UserDetailView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('userdetail/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
]
