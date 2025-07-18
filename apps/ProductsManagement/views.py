from django.shortcuts import render ,get_object_or_404
from rest_framework.views import APIView ,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import ProductCreateUpdateSerializer,ProductDetailSerializer,ProductImageSerilaizer
from .models import Product, Category , ProductImage
from apps.User.models import User ,UserProfile


class ProductCreateUpdateview(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = ProductCreateUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "message": "Product information saved successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def patch(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductCreateUpdateSerializer(product, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "message": "Product information updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)
        product.delete()
        return Response({
            "message": "Product deleted successfully"
        }, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductDetailSerializer(product)
        return Response({
            "message": "Product details fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductDetailSerializer(products, many=True)
        return Response({
            "message": "All product information fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

