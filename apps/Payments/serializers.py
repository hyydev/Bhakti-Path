# serializers.py
from rest_framework import serializers
from .models import Payment
from apps.Order.models import Order

class PaymentSerializer(serializers.ModelSerializer):
    
    order_id = serializers.IntegerField(write_only=True)
    payment_method = serializers.ChoiceField(choices=Payment.PAYMENT_METHODS, required=True)
    payment_status = serializers.CharField(read_only=True)
    payment_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)


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
            payment_amount=order.total_amount,   
            payment_status="PENDING"   
        )

class PaymentVerifySerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)
    razorpay_payment_id = serializers.CharField(required=True)
    razorpay_order_id = serializers.CharField(required=True, write_only=True)
    razorpay_signature = serializers.CharField(required=True, write_only=True)

    def validate_order_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("Invalid order ID")
        return value

    def validate_razorpay_payment_id(self, value):
        if not value.startswith('pay_'):
            raise serializers.ValidationError("Invalid Razorpay payment ID format")
        return value

    def validate_razorpay_order_id(self, value):
        if not value.startswith('order_'):
            raise serializers.ValidationError("Invalid Razorpay order ID format")
        return value
    
    