from django.shortcuts import render
from rest_framework.views import APIView ,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serilaizers import ProductCreateUpdateSerializer,ProductDetailSerializer
from .models import Product, Category , ProductImage
from apps.User.models import User ,UserProfile



class ProductCreateUpdateview(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self,request):

        serializer  = ProductCreateUpdateSerializer(data=request.data)

        if not serializer.is_valid():
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "message": "Product information saved sucessfully ",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

    
    def patch(self,request,id):

        product_id = Product.objects.get(id=id)
        serializer = ProductCreateUpdateSerializer(product_id ,data=request.data(),Partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "message": "Product information updated  sucessfully ",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

    
    def delete(self,request,id):

        product_id = Product.objects.get(id=id)
        product_id.delete()

        return Response({
            "message":"Product information deleted sucessfully " ,
            
        },status=status.HTTP_200_OK)

        

    
class ProductDetailView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self ,id):

        product_id =Product.objects.get(id=id)
        serializer = ProductDetailSerializer(product_id)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({
                "message": "Product detials fetch sucessfully ",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
      
            
           
        

    
class ProductListView(APIView):
    def get(self):

        all_products = Product.object.all()
        serializer = ProductDetailSerializer(all_products)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "message": "Product information updated  sucessfully ",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        

        
     

            

