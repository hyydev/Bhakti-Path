from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, mobile_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name,
            mobile_number=mobile_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, full_name, mobile_number, password, **extra_fields)

class Baseclass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        verbose_name = 'Base Class'


class User(AbstractBaseUser, Baseclass, PermissionsMixin):
    """
    User model for the application.
    """
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'mobile_number']
    objects = UserManager() 

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

