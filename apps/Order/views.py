from django.shortcuts import render

from rest_framework.views import APIView ,status
from  rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import AddtoCartItemSerilaizer,CartItemDetailSerializer
from .models import CartItem,Cart



class AddtoCartView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self , request):

        serializer = AddtoCartItemSerilaizer(data=request.data,context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
        cart_items =  serializer.save()
        return Response({
                "message": "Products added to cart successfully.",
                "cart" : {
                       "id": cart_items[0].cart.id if cart_items else None,
                       "user": request.user.full_name,
                       "items": [
                            {
                                "product_id": ci.product.id,
                                "product_title": ci.product.title,
                                "quantity": ci.quantity,
                                "price_at_time": ci.price_at_time,
                                "total_price": ci.total_price
                            } for ci in cart_items
                        ]
            }
        }, status=status.HTTP_201_CREATED)
    

    def patch(self, request):
      
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddtoCartItemSerilaizer(
            cart,  # instance = cart
            data=request.data,
            context={'request': request},
            partial=True
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        updated_items = serializer.save()

        return Response(
            {
                "message": "Your cart has been updated successfully",
                "cart": {
                    "id": cart.id,
                    "user": request.user.full_name,
                    "items": [
                        {
                            "product_id": ci.product.id,
                            "product_title": ci.product.title,
                            "quantity": ci.quantity,
                            "price_at_time": ci.price_at_time,
                            "total_price": ci.total_price
                        } for ci in updated_items
                    ]
                }
            },
            status=status.HTTP_200_OK
        )

    
    
class CartDetailView(APIView):

    permission_classes = [IsAuthenticated]

    
    def get(self,request):

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serilaizer = CartItemDetailSerializer(cart)

        return Response(serilaizer.data , status=status.HTTP_200_OK)
    

    def delete(self, request, product_id):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return Response({"message": "Product removed from cart"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"message": "Item not found in your cart"}, status=status.HTTP_404_NOT_FOUND)
    

        
class CartClearView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart.cart_item.all().delete()

            return Response({"message": "Cart cleared successfully"}, status=status.HTTP_204_NO_CONTENT)
        
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)



        
        


        

        




        

      


       
    


     


                
    


    
        





