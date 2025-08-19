from django.db import models
from apps.User.models import Baseclass,User,UserAddress
from apps.ProductsManagement.models import Product



class Cart(Baseclass):

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='cart')

    def __str__(self):
        return f"Cart of {self.user.full_name}"
    
    

class CartItem(Baseclass):

    cart =models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_item')
    product = models.ForeignKey(Product,related_name='cartitem',on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('cart', 'product')
        indexes = [
            models.Index(fields=['cart']),
            models.Index(fields=['product']),
        ]

    @property
    def total_price(self):
        return self.price_at_time * self.quantity
    
    def save(self, *args, **kwargs):
        if not self.price_at_time:
            self.price_at_time = self.product.price
        super().save(*args, **kwargs)



class Order(Baseclass):

    ORDER_STATUS = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    order_number = models.CharField(max_length=20,unique=True)
    status = models.CharField(max_length=250,choices=ORDER_STATUS,default='PENDING')
    shipping_address = models.ForeignKey(UserAddress,on_delete=models.SET_NULL,null=True,blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='UNPAID')  # UNPAID / PAID / FAILED
    payment_method = models.CharField(max_length=20, null=True, blank=True)  # e.g. card, upi, cod


    def __str__(self):

        return f"Order {self.order_number} - {self.user.full_name}"
        


class OrderItem(Baseclass):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.price_at_time * self.quantity

     
    



