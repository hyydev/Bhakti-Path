from django.shortcuts import render,get_object_or_404

from rest_framework.views import APIView ,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from decimal import Decimal
from django.db import transaction
from  django.core.cache import cache
from .serializers import AddtoCartItemSerilaizer,CheckoutValidateSerializer
from .models import CartItem,Cart,Order,OrderItem
from .utils import get_cart_from_cache,set_cart_cache,delete_cart_cache,build_cart_payload


class AddtoCartView(APIView):

    permission_classes = [IsAuthenticated]


    @transaction.atomic
    def post(self, request):

        serializer = AddtoCartItemSerilaizer(
            data=request.data, 
            context={'request': request}
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     

        cart = serializer.save()  

        payload = build_cart_payload(cart)

        set_cart_cache(request.user.id, payload)

        return Response({
            "message": "Products added to cart successfully.",
            **payload
        }, status=status.HTTP_201_CREATED)


   
    @transaction.atomic
    def patch(self, request):

        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
      
        serializer = AddtoCartItemSerilaizer(
            cart, 
            data=request.data,
            context={'request': request},
            partial=True
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        updated_cart = serializer.save()
        payload = build_cart_payload(updated_cart)
        set_cart_cache(request.user.id, payload)
        return Response({
            "message": "Cart updated successfully.",
            **payload
            }, status=status.HTTP_200_OK)

      

    
    
class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]
    

    @transaction.atomic
    def get(self, request):

        user = request.user
        cached = get_cart_from_cache(user.id)
        if cached:
            return Response(cached, status=status.HTTP_200_OK)
        
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        payload = build_cart_payload(cart)
        set_cart_cache(user.id, payload)

        return Response(payload, status=status.HTTP_200_OK)
    


    @transaction.atomic
    def delete(self, request, product_id):

        cart = Cart.objects.filter(user =request.user).first()
        if not cart:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
     

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()


            payload = build_cart_payload(cart)
            set_cart_cache(request.user.id, payload)
            return Response({"message": "Item removed from cart",**payload}, status=status.HTTP_200_OK)
            
        except CartItem.DoesNotExist:
            
            return Response({"message": "Item not found in your cart"}, status=status.HTTP_404_NOT_FOUND)
    

        
class CartClearView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def delete(self, request):

        cart = Cart.objects.filter(user=request.user).first()

        if not cart:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        
        cart.cart_item.all().delete()

        delete_cart_cache(request.user.id)

        payload = {
            "cart_id": cart.id,
            "total_price": "0.00",
            "items": []
        }

        return Response({"message": "Cart cleared",**payload}, status=status.HTTP_200_OK)
        


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutValidateSerializer(data=request.data, context={"request": request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart_payload = serializer.validated_data["cart_payload"]
        shipping_address = serializer.validated_data["shipping_address"]
        user = request.user

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                shipping_address=shipping_address,
                total_amount=Decimal(cart_payload["cart"]["total_price"]),
                status="pending",
            )

            for item in cart_payload["cart"]["items"]:
                OrderItem.objects.create(
                    order=order,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    price_at_time=Decimal(item["product_price"]),
                )

            # Clear cart
            delete_cart_cache(user.id)
            Cart.objects.filter(user_id=user.id).delete()

        
        return Response({
            "message": "Order placed successfully",
            "order": {
                "id": order.id,
                "status": order.status,
                "total_amount": str(order.total_amount),
                "shipping_address": {
                    "id": shipping_address.id,
                    "line1": shipping_address.address_line_1,
                    "city": shipping_address.city,
                    "pincode": shipping_address.postal_code,
                },
                "items": cart_payload["cart"]["items"],
            }
        }, status=status.HTTP_201_CREATED)
