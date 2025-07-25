from django.urls import path 
from .views import ProductCreateUpdateview,ProductListView,ProductDetailView



urlpatterns = [

path('create-product/',ProductCreateUpdateview.as_view(),name = 'Product-creation'),
path('update-product/<int:id>',ProductCreateUpdateview.as_view(),name='Product-updation'),
path('delete-product/<int:id>',ProductCreateUpdateview.as_view(),name= 'Product-deletion'),

path('all-product/',ProductListView.as_view(),name= 'allproduct-listing'),
path('get-product/<int:id>',ProductDetailView.as_view(),name='Single-product')


]