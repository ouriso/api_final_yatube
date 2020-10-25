from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Comment, Follow, Group, Post


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'post', 'created')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username'
    )

    def validate(self, data):
        follower = self.context['request'].user
        following = data['following']
        is_follow = Follow.objects.filter(
            user=follower, following=following
        ).exists()
        if follower == following:
            raise serializers.ValidationError("You can't follow yourself")
        if is_follow:
            raise serializers.ValidationError("This follow already exists")
        return data

    class Meta:
        model = Follow
        fields = ('user', 'following')
