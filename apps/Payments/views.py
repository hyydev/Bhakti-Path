from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView ,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from .serializers import PaymentSerializer,PaymentVerifySerializer
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




class RazorpayPaymentVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Step 1: Validate request
        serializer = PaymentVerifySerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        order_id = data["order_id"]
        razorpay_payment_id = data["razorpay_payment_id"]
        razorpay_order_id = data["razorpay_order_id"]
        razorpay_signature = data["razorpay_signature"]

        # Step 2: Fetch payment record
        try:
            payment = Payment.objects.get(
                order_id=order_id,
                razorpay_order_id=razorpay_order_id
            )
        except Payment.DoesNotExist:
            return Response(
                {"error": "Payment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Step 3: Verify Razorpay signature
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            })
            verified = True
        except:
            verified = False

        # Step 4: Update via service
        order = payment.order
        response_data = Payment_services.handle_razorpay_verify(
            order, payment, razorpay_payment_id, razorpay_signature, verified
        )

        # Step 5: Return response
        if verified:
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class RazorpayWebhookView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        raw_body = request.body.decode("utf-8")
        signature_header = request.headers.get("X-Razorpay-Signature", "")
        payload = request.data

        # Log webhook for audit
        print("Razorpay Webhook received:", payload)
        print("Signature header:", signature_header)

        # Step 1: Verify webhook signature
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        try:
            client.utility.verify_webhook_signature(
                raw_body,
                signature_header,
                settings.RAZORPAY_WEBHOOK_SECRET
            )
            verified = True
            print("Webhook signature verified")
        except Exception as e:
            verified = False
            print("Webhook verification failed:", str(e))
            return Response(
                {"error": "invalid_signature"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Step 2: Extract payment details from payload
        razorpay_order_id = payload.get("payload", {}).get("payment", {}).get("entity", {}).get("order_id")
        razorpay_payment_id = payload.get("payload", {}).get("payment", {}).get("entity", {}).get("id")

        if not razorpay_order_id:
            return Response(
                {"error": "missing_order_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Step 3: Fetch payment record
        try:
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            order = payment.order
        except Payment.DoesNotExist:
            print("Payment not found for razorpay_order_id:", razorpay_order_id)
            return Response(
                {"error": "Payment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Step 4: Update via service
        razorpay_signature = payload.get("payload", {}).get("payment", {}).get("entity", {}).get("signature", signature_header)
        
        result = Payment_services.handle_razorpay_verify(
            order, payment, razorpay_payment_id, razorpay_signature, verified
        )

        return Response({"data": result}, status=status.HTTP_200_OK)