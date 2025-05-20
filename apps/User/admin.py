from django.contrib import admin
from .models import User, UserProfile, UserAddress

admin.site.register(User)

admin.site.register(UserProfile)

admin.site.register(UserAddress)



# Register your models here.
