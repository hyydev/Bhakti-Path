from .models import Payment
from apps.Order.models import Order
from django.conf import settings


class Payment_services:

    @staticmethod
    def handle_cod(order, payment):

        order.status = "PLACED"
        order.payment_status = "PAID"
        order.save(update_fields=["status", "payment_status"])

        payment.payment_status = "SUCCESS"
        payment.save(update_fields=["payment_status"])

        return {
            "message": "Payment confirmed via COD",
            "order_id": order.id,
            "status": order.status,
            "payment": {
                "method": payment.payment_method,
                "status": payment.payment_status,
                "amount": str(payment.payment_amount),
            },
        }

    @staticmethod
    def handle_razorpay(order, payment, razorpay_order):

        payment.razorpay_order_id = razorpay_order["id"]
        payment.payment_status = "PENDING"
        payment.save(update_fields=["razorpay_order_id", "payment_status"])

        return {
            "message": "Razorpay order initiated",
            "order_id": order.id,
            "status": order.status,
            "payment": {
                "method": payment.payment_method,
                "status": payment.payment_status,
                "razorpay_order_id": razorpay_order["id"],
                "currency": razorpay_order["currency"],
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "amount": razorpay_order["amount"],
            },
        }


    @staticmethod
    def handle_razorpay_verify(
        order, payment, razorpay_payment_id, razorpay_signature, verified
    ):

        payment.razorpay_payment_id = razorpay_payment_id

        # Sirf agar signature hai toh store karo (verify API se aata hai, webhook se nahi)
        if razorpay_signature:
            payment.razorpay_signature = razorpay_signature

        if verified:
            # Idempotency check — already PLACED hai toh dobara mat update karo
            if order.status == "PLACED" and order.payment_status == "PAID":
                return {
                    "message": "Payment already verified",
                    "order_id": order.id,
                    "status": order.status,
                }

            order.status = "PLACED"
            order.payment_status = "PAID"
            order.save(update_fields=["status", "payment_status"])

            payment.payment_status = "SUCCESS"
            save_fields = ["razorpay_payment_id", "payment_status"]
            if razorpay_signature:
                save_fields.append("razorpay_signature")
            payment.save(update_fields=save_fields)

            return {
                "message": "Payment successful via Razorpay",
                "order_id": order.id,
                "status": order.status,
                "payment": {
                    "method": payment.payment_method,
                    "status": payment.payment_status,
                    "amount": str(payment.payment_amount),
                    "razorpay_payment_id": payment.razorpay_payment_id,
                },
            }
        else:
            payment.payment_status = "FAILED"
            payment.save(update_fields=["razorpay_payment_id", "payment_status"])

            order.payment_status = "FAILED"
            order.save(update_fields=["payment_status"])

            return {
                "message": "Payment verification failed",
                "order_id": order.id,
                "status": order.status,
            }
