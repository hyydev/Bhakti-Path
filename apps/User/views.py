from rest_framework.response import Response
from rest_framework.views import APIView ,status
from .serializers import UserSerializer, UserProfileSerializer , UserAddresssSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User



class UserRegisterView(APIView):
    """
    API view to register a new user.
    """
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({
            "message": "User registered successfully. OTP send"}, 
             status=status.HTTP_201_CREATED)
        

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"message":"All Users Details fetched sucessfully",
                         "data":serializer.data}, 
                         status=status.HTTP_200_OK)
    

class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    """
    API  view to retrieve, update or delete a user.
    """
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response({
        "message": "  User Detail fetched successfully",
        "data": serializer.data
            }, status=status.HTTP_200_OK)
    


    def patch(self, request, user_id):
        user =User.objects.get(id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "message": "User updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

    

    def delete(self, request, user_id):
        user =User.objects.get(id=user_id)
        user.delete()
        return Response({
            "message": "User deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)



class AllUserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser] 
    """
    API view to retrieve all user profiles.
    """

    def get(self, request):
        users = User.objects.all()
        profiles = [user.profile for user in users if hasattr(user, 'profile')]
        serializer = UserProfileSerializer(profiles, many=True)
        return Response({
            "message": "All User Profiles fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
       
class UserProfileView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser,IsAuthenticated] 

    """
    API view to retrieve user profile.
    """

    def get(self, request,id):
        user =User.objects.get(id=id)
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if  request.user != user:
            return Response({"message": "You are not authorized to view this profile"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UserProfileSerializer(user.profile)
        return Response({
            "message": "User profile fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
       
    
    def patch(self, request,id):
        """
        API view to update user profile.
        """
        
        user = User.objects.get(id=id)
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != user:
            return Response({"message": "You are not authorized to update this profile"}, status=status.HTTP_403_FORBIDDEN)

        serilaizer = UserProfileSerializer(user.profile,data=request.data, partial=True)

        if not serilaizer.is_valid():
            return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serilaizer.save()

        return Response({
            "message": "User profile updated successfully",
            "data": serilaizer.data
        }, status=status.HTTP_200_OK)
    


class UserAddressView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 

    """
    API view to retrieve user address.
    """

    def get(self,request):
        user = request.user
        if not hasattr(user, 'profile'):
            return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Fetching the user profile
        user_profile = user.profile
        if not user_profile:
            return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        addresses = user.profile.addresses.all()
        serializer = UserAddresssSerializer(addresses, many=True)
        return Response({
            "message": "User addresses fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

    def post(self, request):
        user = request.user
        if not hasattr(user, 'profile'):
            return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserAddresssSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        if serializer.validated_data.get('is_default', False):
            user.profile.addresses.update(is_default=False)

        serializer.save(user_profile=user.profile)
        return Response({
            "message": "User address created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def patch(self, request, address_id):
        user = request.user
        if not hasattr(user, 'profile'):
            return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
        address = user.profile.addresses.filter(id=address_id).first()
        if not address:
            return Response({"message": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserAddresssSerializer(address, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "message": "User address updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, address_id):
        user = request.user
        if not hasattr(user, 'profile'):
            return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        address = user.profile.addresses.filter(id=address_id).first()
        if not address:
            return Response({"message": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        
        address.delete()
        return Response({
            "message": "User address deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)
    
class SetDefaultAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, address_id):
        user = request.user
        if not hasattr(user, 'profile'):
            return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        address = user.profile.addresses.filter(id=address_id).first()
        if not address:
            return Response({"message": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Set all addresses to not default
        user.profile.addresses.update(is_default=False)
        
        # Set the selected address as default
        address.is_default = True
        address.save()
        
        return Response({"message": "Default address set successfully"}, status=status.HTTP_200_OK)
    
    
