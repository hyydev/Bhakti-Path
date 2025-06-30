from django.urls import path
from .views import UserRegisterView, UserDetailView, UserProfileView ,AllUserProfileView ,UserAddressView, SetDefaultAddressView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('userdetail/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),

    path('userprofile/', AllUserProfileView.as_view(), name='all-user-profile'),
    path('userprofile/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),

    path('useraddresses/', UserAddressView.as_view(), name='user-addresses'),
    path('useraddresses/<int:address_id>/', UserAddressView.as_view(), name='user-address-detail'),
    path('set-default-address/<int:address_id>/', SetDefaultAddressView.as_view(), name='set-default-address'),
    
]
