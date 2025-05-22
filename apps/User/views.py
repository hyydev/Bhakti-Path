from rest_framework.response import Response
from rest_framework.views import APIView ,status
from .serializers import UserSerializer
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
        pass
       
