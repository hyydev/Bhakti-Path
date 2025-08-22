from .models import Payment
from apps.Order.models import Order



class Payment_services:
    
    @staticmethod
    def handle_cod(order,payment):

        order.status = "PLACED"
        order.payment_status = "PAID"
        order.save(update_fields=["status","payment_status"])

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
            }
        }



    


        