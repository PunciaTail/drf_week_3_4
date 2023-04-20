from rest_framework import serializers
from articles.models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
    #시리얼라이저에서 메서드를 호출하여 필드의 값을 결정한다
    user = serializers.SerializerMethodField()
    
    #여기 메서드 호출
    def get_user(self, obj):
        return obj.user.email
    
    class Meta:
        model = Comment
        exclude = ('article',)


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)


class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # 역참조
    comment_set = CommentSerializer(many = True)
    likes = serializers.Serializer(many=True)

    def get_user(self, obj):
        return obj.user.email
    
    class Meta:
        model = Article
        fields = '__all__'


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'image', 'content')


class ArticleListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    # user attribute(변수) 앞에 get을 사용
    # obj는 해당 Article
    def get_user(self, obj):
        # return 값이 user라는 attribute 값에 들어감
        return obj.user.email
    
    def get_like_count(self, obj):
        return obj.likes.count()
    
    def get_comment_count(self, obj):
        return obj.comment_set.count()
    
    class Meta:
        model = Article
        fields = ('id', 'title', 'user', 'updated_at', 'like_count', 'comment_count')