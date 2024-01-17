from rest_framework.viewsets import ModelViewSet

from .models import Category, Post
from .serializers import CategorySerializer, PostSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
