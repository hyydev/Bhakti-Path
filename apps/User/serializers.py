from rest_framework import serializers
from .models import User, UserProfile, UserAddress
from apps.Auth.models import OTPVerification
import random

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    full_name = serializers.CharField(max_length=255,required=True)
    email = serializers.EmailField(required=True)
    mobile_number = serializers.CharField(max_length=10,required=True)
    password = serializers.CharField(max_length=255, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'mobile_number', 'password', 'is_active', 'is_verified']
        
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
            'is_verified': {'read_only': True},
            
        }

    def validate_password(self, value):

        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        for char in value:
            if not char.isalnum():
                raise serializers.ValidationError("Password must contain only alphanumeric characters.")
        return value


    def validate_email(self, value):
        email = User.objects.filter(email=value).exists()
        if email:
            raise serializers.ValidationError("Email already exists.")
        return value


    def validate_mobile_number(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("Mobile number must be 10 digits long.")
        if not value.isdigit():
            raise serializers.ValidationError("Mobile number must contain only digits.")
        
        mobile_number = User.objects.filter(mobile_number=value).exists()
        if mobile_number:
            raise serializers.ValidationError("Mobile number already exists.")
        
        return value
        

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = False
        user.is_verified = False
        user.save()

        # OTP generation and sending logic can be added here
        otp_code = (random.randint(100000, 999999))
        print(f"OTP for {user.email}: {otp_code}")

        # Save OTP to the database
        otp_verification = OTPVerification.objects.create(
            user=user,
            otp_code=otp_code,
            email=user.email,
            mobile_number=user.mobile_number,
            attempt_count=0,
            expired_at=None, # Set the expiration time as needed
            is_verified=False
        )
        otp_verification.save()

        return user
    
