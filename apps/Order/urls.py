from django.urls import path
from .views import AddtoCartView,CartDetailView

urlpatterns = [
    
path('add-to-cart/',AddtoCartView.as_view(),name = 'Add to cart '),
path('cart-detail/',CartDetailView.as_view(),name='cart-detail'),
path('update-cart/',AddtoCartView.as_view(),name='cart-update'),
path('delete-cart/<int:product_id>',CartDetailView.as_view(),name='cart-delete'),


]