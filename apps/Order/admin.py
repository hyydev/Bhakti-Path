from django.contrib import admin
from .models import Order,OrderItem,Cart,CartItem


admin.site.register(Cart)
admin.site.register(Order)

