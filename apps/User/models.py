from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Baseclass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        verbose_name = 'Base Class'


class User(AbstractBaseUser, Baseclass):
    """
    User model for the application.
    """
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'user'


class UserProfile(Baseclass):
    """
    User profile model for additional user information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='user_profile_pictures/', null=True, blank=True)
    gender = models.CharField(max_length=10,null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    user_address = models.ForeignKey('UserAddress', on_delete=models.CASCADE, null=True, blank=True)

 


    def __str__(self):
        return f"{self.user.full_name}'s Profile"
    
    class Meta:
        db_table = 'user_profile'
        ordering = ['-created_at']


class UserAddress(Baseclass):
    """
    User address model for storing user addresses.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.full_name}'s Address"
    
    class Meta:
        db_table = 'user_address'
        ordering = ['-created_at']

