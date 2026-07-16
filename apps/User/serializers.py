from rest_framework import serializers
from .models import User, UserProfile, UserAddress
from apps.Auth.models import OTPVerification
from django.utils import timezone
from .email_utils import send_otp_email
from datetime import timedelta
import logging
import random

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    full_name = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True)
    mobile_number = serializers.CharField(max_length=10, required=True)
    password = serializers.CharField(max_length=255, write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "mobile_number",
            "password",
            "is_active",
            "is_verified",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "is_active": {"read_only": True},
            "is_verified": {"read_only": True},
        }

    def validate_password(self, value):

        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        for char in value:
            if not char.isalnum():
                raise serializers.ValidationError(
                    "Password must contain only alphanumeric characters."
                )
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
        user.set_password(validated_data["password"])
        user.is_active = False
        user.is_verified = False
        user.save()

        # Step 2: Random OTP
        otp_code = str(random.randint(100000, 999999))

        otp_verification = OTPVerification.objects.create(
            user=user,
            otp_code=otp_code,
            email=user.email,
            mobile_number=user.mobile_number,
            attempt_count=0,
            expired_at=timezone.now() + timedelta(minutes=5),
            is_verified=False,
        )
        otp_verification.save()

        # Step 4: Email bhejo
        email_sent = send_otp_email(
            user_email=user.email,
            user_name=user.full_name,
            otp_code=otp_code,
        )

        if not email_sent:
            logger.error(f"OTP email failed for {user.email}")

        return user


class UserAddresssSerializer(serializers.ModelSerializer):
    """
    Serilaizer for the UserAddress model.

    """

    class Meta:
        model = UserAddress
        fields = [
            "id",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "country",
            "postal_code",
            "is_default",
        ]
        extra_kwargs = {
            "user_profile": {"read_only": True},
            "is_default": {"required": False},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.
    """

    user = UserSerializer(read_only=True)
    addresses = UserAddresssSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "user",
            "profile_picture",
            "date_of_birth",
            "gender",
            "addresses",
        ]
