from django.db import models
from apps.User.models import Baseclass,User
from apps.ProductsManagement.models import Product



class Cart(Baseclass):

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='cart')



    def __str__(self):
        return f"Cart of {self.user.username}"
    
    

class CartItem(Baseclass):

    cart =models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_item')
    product = models.ForeignKey(Product,related_name='cartitem',on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.price_at_time * self.quantity
    
    def save(self, *args, **kwargs):
        if not self.price_at_time:
            self.price_at_time = self.product.price
        super().save(*args, **kwargs)

        




  






