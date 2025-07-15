from django.urls import path 
from .views import ProductCreateUpdateview,ProductListView,ProductDetailView



urlpatterns = [

path('create-product/',ProductCreateUpdateview.as_view(),name = 'Product-creation'),
path('update-product/<int:product_id>',ProductCreateUpdateview.as_view(),name='Product-updation'),
path('delete-product/<int:product_id>',ProductCreateUpdateview.as_view(),name= 'Product-deletion'),

path('all-product/',ProductListView.as_view(),name= 'allproduct-listing'),
path('product/<int:product_id>',ProductDetailView.as_view(),name='Single-product')


]