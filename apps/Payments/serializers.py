# serializers.py
from rest_framework import serializers
from .models import Payment
from apps.Order.models import Order

class PaymentSerializer(serializers.ModelSerializer):
    
    order_id = serializers.IntegerField(write_only=True)
    payment_method = serializers.ChoiceField(choices=Payment.PAYMENT_METHODS, required=True)

    class Meta:
        model = Payment
        fields = ["order_id", "payment_method", "payment_status", "payment_amount"]
        read_only_fields = ["payment_status", "payment_amount"]

    def validate(self, attrs):

        order_id = attrs.get("order_id")
        user = self.context["request"].user

        order = Order.objects.select_related("user").filter(id=order_id).first()

        if not order:
            raise serializers.ValidationError({"order_id": "Invalid order ID"})
        
        if order.user_id != user.id:
            raise serializers.ValidationError({"order_id": "This order does not belong to you"})
        
        if Payment.objects.filter(order_id=order_id).exists():
            raise serializers.ValidationError({"order_id": "Payment already exists"})

        attrs["order"] = order
        return attrs

    def create(self, validated_data):

        order = validated_data.pop("order")
        return Payment.objects.create(
            order=order,
            user=order.user,
            payment_method=validated_data["payment_method"],
            payment_status="INITIATED",
            payment_amount=order.total_amount
        )
