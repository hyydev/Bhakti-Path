from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView ,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import PaymentSerializer
from .services import Payment_services
import razorpay
from django.conf import settings
from .models import Payment


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

            elif method == "RAZORPAY":
                 
                 client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                 razorpay_order = client.order.create({
                    "amount": int(order.total_amount * 100),
                    "currency": "INR",
                    "payment_capture": 1
                 })

                 response = Payment_services.handle_razorpay(order,payment,razorpay_order)


            else:
                   
                return Response({"error": "Unsupported payment method"},
                                status=status.HTTP_400_BAD_REQUEST)
            

        return Response(response, status=status.HTTP_201_CREATED)





# class RazorpayWebhookView(APIView):
    
#     def post(self, request):
#         payload = request.data

#         razorpay_order_id = payload.get("payload", {}).get("payment", {}).get("entity", {}).get("order_id")
#         razorpay_payment_id = payload.get("payload", {}).get("payment", {}).get("entity", {}).get("id")
#         razorpay_signature = request.headers.get("X-Razorpay-Signature")

#         # Verify Signature
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         try:

#             client.utility.verify_webhook_signature(
#                 request.body.decode("utf-8"), 
#                 razorpay_signature, 
#                 settings.RAZORPAY_WEBHOOK_SECRET
#             )
#             verified = True
#         except:
#             verified = False


#         # Payment Update service ko call karo
#         payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
#         order = payment.order


#         data = Payment_services.handle_razorpay_verify(
#             order, payment, razorpay_payment_id, razorpay_signature, verified

#         )

#         return Response({
#             "data":data , 
#             "status":status.HTTP_200_OK
#         })




        
class RazorpayWebhookView(APIView):
    
    def post(self, request):
        payload = request.data
        print("🔔 Incoming Webhook Payload:", payload)   # 👈 yeh add kar

        razorpay_order_id = payload.get("payload", {}).get("payment", {}).get("entity", {}).get("order_id")
        razorpay_payment_id = payload.get("payload", {}).get("payment", {}).get("entity", {}).get("id")
        razorpay_signature = request.headers.get("X-Razorpay-Signature")
        print("🔑 Signature from Header:", razorpay_signature)   # 👈 yeh bhi add kar

        # Verify Signature
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_webhook_signature(
                request.body.decode("utf-8"), 
                razorpay_signature, 
                settings.RAZORPAY_WEBHOOK_SECRET
            )
            verified = True
            print("✅ Webhook Signature Verified")
        except Exception as e:
            verified = False
            print("❌ Webhook Verification Failed:", str(e))

        # Payment Update service ko call karo
        try:
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            order = payment.order
        except Payment.DoesNotExist:
            print("⚠️ Payment not found for order:", razorpay_order_id)
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        data = Payment_services.handle_razorpay_verify(
            order, payment, razorpay_payment_id, razorpay_signature, verified
        )

        return Response({
            "data": data, 
            "status": status.HTTP_200_OK
        })


   

    


