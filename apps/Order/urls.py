from django.urls import path
from .views import AddtoCartView,CartDetailView,CartClearView

urlpatterns = [
    
path('add-to-cart/',AddtoCartView.as_view(),name = 'Add to cart '),
path('cart-detail/',CartDetailView.as_view(),name='cart-detail'),
path('update-cart/',AddtoCartView.as_view(),name='cart-update'),
path('delete-cart/<int:product_id>',CartDetailView.as_view(),name='cart-delete'),
path('clear-cart/',CartClearView.as_view(),name='clear-cart')


]