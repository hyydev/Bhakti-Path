from rest_framework import serializers
from .models import OTPVerification
from apps.User.models import User


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
    


        

    


     

        

       


        

        
    
   