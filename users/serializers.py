from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from users.models import User
from articles.serializers import ArticleListSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    # 해당 모델의 __str__() 메서드를 호출하여 문자열로 표현된 관련 객체를 반환
    # PrimaryKeyRelatedField 는 아이디로 보여줌 // read_only=True
    followers = serializers.StringRelatedField(many=True)
    followings = serializers.StringRelatedField(many=True)
    #related_name이나 set으로 참조
    article_set = ArticleListSerializer(many=True)
    like_user = ArticleListSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'followings', 'followers', 'article_set', 'like_user')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        # 해싱
        user.set_password(password)
        user.save()
        return user
    
    def update(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user
    



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email

        return token