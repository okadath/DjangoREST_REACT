from rest_framework import generics

from .models import Post
#from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer
from rest_framework import permissions


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer