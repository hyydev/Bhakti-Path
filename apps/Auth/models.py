from django.db import models
from apps.User.models import Baseclass,User


class OTPVerification(Baseclass):
    """
    OTP Verification model for user authentication.
    """
    id =models.UUIDField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_verification')
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    expired_at = models.DateTimeField()
    attempt_count = models.IntegerField(default=0)


    def __str__(self):
        return f"OTP for {self.user.full_name}"
    
    class Meta:
        db_table = 'otp_verification'
        ordering = ['-created_at']


