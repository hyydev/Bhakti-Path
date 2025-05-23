from django.shortcuts import render
from rest_framework.views import APIView ,status
from rest_framework.response import Response
from .serializers import OTPVerificationSerializer, UserloginSerializer ,UserlogoutSerializer
from .models import OTPVerification



class VerifyOtpView(APIView):
    """
    API view to verify otp 
    """
    def post(self,request):
        serializer = OTPVerificationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        otp_obj = serializer.validated_data['otp_obj']
        otp_obj.is_verified = True
        otp_obj.save()
        
        return Response({
            "message": "OTP verified successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    
class ResendOtpView(APIView):
    pass


class UserLoginView(APIView):
    """
    API view to login user
    """
    def post(self,request):
        serializer = UserloginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "message": "User logged in successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
        
class UserLogoutView(APIView):

    def post(self,request):
        """
        API view to logout user
        """
        serializer = UserlogoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "message": "User logged out successfully",
        }, status=status.HTTP_200_OK)
