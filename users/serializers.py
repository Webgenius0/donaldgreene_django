from .models import User
from rest_framework import fields, serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email",  "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        if validate_password(validated_data["password"]) == None:
            password = make_password(validated_data["password"])
            user = User.objects.create(
                email=validated_data["email"],
                password=password,
            )
            return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "state", "city", "bio", "age", "gender", "is_active"]
        # fields = "__all__"


# reset password new to old password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
