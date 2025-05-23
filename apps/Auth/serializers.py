from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTPVerification
from apps.User.models import User
from django.db.models import Q


class OTPVerificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the OTPVerification model.
    """
    email = serializers.EmailField(required=True)
    mobile_number = serializers.CharField(max_length=15, required=True)
    otp_code = serializers.CharField(max_length=6, required=True)

    class Meta:
        model = OTPVerification
        fields = ['id', 'user', 'email', 'mobile_number', 'otp_code',]
        extra_kwargs = {
        'user': {'read_only': True}  
    }


    def validate_otp_code(self, value):
        if len(value) != 6:
            raise serializers.ValidationError("OTP code must be 6 digits long.")
        if not value.isdigit():
            raise serializers.ValidationError("OTP code must contain only digits.")
        return value
    

    def validate_mobile_number(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("Mobile number must be 10 digits long.")
        if not value.isdigit():
            raise serializers.ValidationError("Mobile number must contain only digits.")
        return value
    
    
    def validate(self,attrs):
        """
        Validate otp_code ,email and mobile_number and check otp_code is correct or not
        """

        otp_code =attrs.get('otp_code')
        email = attrs.get('email')
        mobile_number = attrs.get('mobile_number')

        otp_obj =OTPVerification.objects.filter(
            otp_code=otp_code,
            email=email,
            mobile_number=mobile_number).first()

       

        if not otp_obj:
            raise serializers.ValidationError("Invalid OTP code or email or mobile number.")
        
        user = otp_obj.user

        if not user:
            raise serializers.ValidationError("User not found.")

        if user.is_verified:
            raise serializers.ValidationError("User is already verified.")
        

        user.is_verified = True
        user.save()

        otp_obj.delete()

        attrs['otp_obj'] = otp_obj

        return attrs
    


        

    
class UserloginSerializer(serializers.Serializer):
    """
    Serializer for user login with Jwt authentication.
    """

    email_or_mobile_number = serializers.CharField(required=True,write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    
    def validate(self, attrs):
        email_or_mobile_number = attrs.get('email_or_mobile_number')
        password =attrs.get('password')

        user = User.objects.filter(
            Q(email=email_or_mobile_number) | Q(mobile_number=email_or_mobile_number)
        ).first()

        if not user:
            raise serializers.ValidationError("User not found.")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password.")
        
        if not user.is_verified:
            raise serializers.ValidationError("User is not verified")
        
        if not user.is_active:
            user.is_active = True
            user.save()

        refresh = RefreshToken.for_user(user)
   
        attrs['access_token'] = str(refresh.access_token)
        attrs['refresh_token'] = str(refresh)
        attrs['is_verified'] = user.is_verified
        attrs['is_active'] = user.is_active
        return attrs
    
    
        

class UserlogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout with Jwt authentication.
    """
    refresh_token = serializers.CharField(required=True, write_only=True)

    def validate(self,attrs):
        refresh_token=(attrs.get('refresh_token'))
        if not refresh_token:
            raise serializers.ValidationError("Refresh token is required.")
        
        token=RefreshToken(refresh_token)
        if not token:
            raise serializers.ValidationError("Invalid refresh token.")
        
        if token.blacklist:
            raise serializers.ValidationError("Refresh token is already blacklisted.")
        
        token.blacklist()

        attrs['refresh_token'] = refresh_token
        return attrs


