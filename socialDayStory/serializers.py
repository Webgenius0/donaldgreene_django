from rest_framework import serializers
from .models import DayStory, DayStoryComment, DayStoryLike, DayStoryShare
# from users.models import User
from users.serializers import UserSerializer


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"


class DayStoryCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DayStoryComment
        # fields = "__all__"
        fields = ["id", "user", "content", "created_at"]


class DayStoryLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DayStoryLike
        fields = ["id", "user", "created_at"]


class DayStoryShareSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DayStoryShare
        # fields = "__all__"
        fields = ["id", "user", "created_at"]


class DayStorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = DayStoryCommentSerializer(many=True, read_only=True)
    likes = DayStoryLikeSerializer(many=True, read_only=True)
    shares = DayStoryShareSerializer(many=True, read_only=True)

    class Meta:
        model = DayStory
        # fields = "__all__"
        fields = ["id", "user", "title", "content", "comments", "likes", "shares"]
