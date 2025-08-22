from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView ,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import PaymentSerializer
from .services import Payment_services



class PaymentInitiateView(APIView):

    def post(self,request):

        serializer = PaymentSerializer(data=request.data,context= {"request":request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        order = serializer.validated_data["order"]
        method = serializer.validated_data["payment_method"]

        with transaction.atomic():

            payment = serializer.save()

            if method == "COD":
                response = Payment_services.handle_cod(order,payment)

            elif method == "Razorpay":
                pass

            else:
                   
                return Response({"error": "Unsupported payment method"},
                                status=status.HTTP_400_BAD_REQUEST)
            

        return Response(response, status=status.HTTP_201_CREATED)







        


   

    


