from rest_framework import serializers
from .models import Post, Comment, Like, Share, PostImage
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


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["id", "image"]



class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    shares = ShareSerializer(many=True, read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    total_likes = serializers.SerializerMethodField()
    total_comment = serializers.SerializerMethodField()
    total_shares = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "images",
            "created_at",
            "updated_at",
            "user",
            "total_comment", 
            "comments",
            "total_likes",
            "likes",
            "total_shares",
            "shares",
        ]
    
    def get_total_likes(self, obj):
        return obj.likes.count()
    def get_total_comment(self, obj):
        return obj.comments.count()
    def get_total_shares(self, obj):
        return obj.shares.count()
