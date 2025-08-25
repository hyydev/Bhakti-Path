from django.db import models
from apps.Order.models import Order 
from apps.User.models import User
from decimal import Decimal
from apps.Auth.models import Baseclass



class Payment(Baseclass):

    PAYMENT_METHODS = [
        ("COD", "Cash on Delivery"),
        ("RAZORPAY", "Razorpay"),
        ("STRIPE", "Stripe"),
        ("PAYPAL", "Paypal"),
    ]

    PAYMENT_STATUS = [
        ("INITIATED", "Initiated"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    ]
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='payment')
    order = models.OneToOneField(Order,on_delete=models.CASCADE, related_name='payment')
    payment_status = models.CharField(max_length=250,choices=PAYMENT_STATUS,default='INITIATED')
    payment_method = models.CharField(max_length = 50,choices=PAYMENT_METHODS)
    payment_amount = models.DecimalField(max_digits=10,decimal_places=2,default=Decimal("00.0"))

    # Razorpay fileds 
    transaction_id = models.CharField(max_length=255, blank=True, null=True)   # UPI txn id, Stripe charge id, etc.
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)







