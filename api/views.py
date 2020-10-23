from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import generics, viewsets, serializers

from rest_framework.filters import SearchFilter

from .models import Follow, Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
)


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('group',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        return post.comments

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowList(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = [SearchFilter]
    search_fields = ['=user__username', '=following__username']

    def perform_create(self, serializer):
        username = self.request.data.get('following')
<<<<<<< HEAD
        try:
            following = User.objects.get(username=username)
        except:
            raise serializers.ValidationError("This user doesn't exists")
        if Follow.objects.filter(
            user=self.request.user, following=following
        ).exists():
            raise serializers.ValidationError("This follow already exists")
=======
        # не понял как это сделать красиво..
        if not User.objects.filter(username=username).exists() or \
           Follow.objects.filter(user=self.request.user, following__username=username).exists():
            raise serializers.ValidationError("This user doesn't exists")
        following = User.objects.get(username=username)
>>>>>>> 0308ada6b55b2e8f34ba43f40b582c95901cfe7c
        serializer.save(user=self.request.user, following=following)
