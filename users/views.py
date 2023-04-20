from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User


# Create your views here.
class UserView(APIView):
    def post(self, request):
        serialize = UserSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response({'message':'가입완료'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':f'${serialize.errors}'}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MockView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response('get 요청')
    

class FollowView(APIView):
    def post (self, request, user_id):
        other = get_object_or_404(User, id=user_id)
        me = request.user
        if me in other.followers.all():
            other.followers.remove(me)
            return Response('언팔', status=status.HTTP_200_OK)
        else:
            other.followers.add(me)
            return Response('팔로우', status=status.HTTP_200_OK)
        
class ProfileView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serialize = UserProfileSerializer(user)
        return Response(serialize.data)