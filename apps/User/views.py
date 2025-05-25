from rest_framework.response import Response
from rest_framework.views import APIView ,status
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User


# Create your views here.


class UserRegisterView(APIView):
    """
    API view to register a new user.
    """
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
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
    permission_classes = [IsAuthenticated] 

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
    

        

