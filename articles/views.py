from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from articles.models import Article, Comment
from articles.serializers import ArticleSerializer, ArticleListSerializer, ArticleCreateSerializer, CommentSerializer, CommentCreateSerializer
from django.db.models.query_utils import Q


class ArticleView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serialize = ArticleListSerializer(articles, many=True)

        return Response(serialize.data, status=status.HTTP_200_OK)

    def post(self, request):

        serialize = ArticleCreateSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save(user=request.user)
            return Response(serialize.data, status=status.HTTP_200_OK)
        else:
            return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        serialize = ArticleSerializer(article)
        return Response(serialize.data, status=status.HTTP_200_OK)

    def put(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            serialize = ArticleCreateSerializer(article, data=request.data)
            
            if serialize.is_valid():
                serialize.save()
                return Response(serialize.data, status=status.HTTP_200_OK)
            else:
                return Response(serialize.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('권한 x', status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            article.delete()
            return Response('삭제되었습니다.', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('삭제 못함', status=status.HTTP_403_FORBIDDEN)


class CommentView(APIView):
    def get(self, request, article_id):
        article = Article.objects.get(id=article_id)
        comments = article.comment_set.all()
        serialize = CommentSerializer(comments, many=True)

        return Response(serialize.data, status=status.HTTP_200_OK)

    def post(self, request, article_id):
        serialize = CommentCreateSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save(user=request.user, article_id=article_id)
            return Response(serialize.data, status=status.HTTP_200_OK)
        else:
            return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serialize = CommentCreateSerializer(comment, data=request.data)
            if serialize.is_valid():
                serialize.save()
                return Response(serialize.data, status=status.HTTP_200_OK)
            else:
                return Response(serialize.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('댓글 권한x', status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response('댓글 삭제 O', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('삭제 권한이 없음', status=status.HTTP_403_FORBIDDEN)


class LikeView(APIView):
    # DB에 들어가면 post
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response('헤어져요', status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response('좋아요', status=status.HTTP_200_OK)
        

class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        q = Q()
        for user in request.user.followings.all():
            q.add(Q(user=user),q.OR)
        feeds = Article.objects.filter(q)
        serialize = ArticleListSerializer(feeds, many =True)
        return Response(serialize.data)