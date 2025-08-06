from django.shortcuts import render ,get_object_or_404
from rest_framework.views import APIView ,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ProductCreateUpdateSerializer,ProductDetailSerializer,ProductImageSerializer
from .models import Product, Category , ProductImage
from apps.User.models import User ,UserProfile
from django.db.models import Q


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

        products = Product.objects.select_related('category').all()

        #Filtering 
        title = request.query_params.get('title')
        product_type = request.query_params.get('product_type')
        category = request.query_params.get('category')
        price_min = request.query_params.get('price_min')
        price_max = request.query_params.get('price_max')

        if title:
            products = products.filter(title__icontains=title)

        if product_type:
            products = products.filter(product_type=product_type)
 
        if category:
            products = products.filter(category_id=category)

        if price_min:
            products = products.filter(price__gte=price_min)

        if price_max:
            products = products.filter(price__lte=price_max)

        #searching 
        search = request.query_params.get('search')
        if search:
            products = products.filter(Q(title__icontains=search) |
                                       Q(description__icontains=search) |
                                       Q(category__name__icontains=search)|
                                       Q(product_type__icontains=search)|
                                       Q(meta_keywords=search))

        serializer = ProductDetailSerializer(products, many=True)

        return Response({
            "message": "All product information fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


