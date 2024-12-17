from rest_framework import serializers
from .models import Post, Comment, Like, Share
# from users.models import User
from users.serializers import UserSerializer


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         # fields = ['id', 'username', 'email']
#         fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ["id", "user", "content", "created_at"]
        


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        fields = ["id", "user", "created_at"]


class ShareSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Share
        fields = ["id", "user", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    shares = ShareSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
            "user",
            "comments",
            "likes",
            "shares",
        ]
