from .models import User, UserConnector
from rest_framework import fields, serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# user serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "state",
            "city",
            "bio",
            "age",
            "gender",
            "occupation",
            "marital_status",
            "language",
            "avater",
            "date_joined",
        ]


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # if validate_password(validated_data["password"]) == None:
        try:
        # Validate password using Django's password validators
            validate_password(validated_data["password"])
        except ValidationError as e:
        # Raise the validation errors as JSON-friendly response
            raise serializers.ValidationError({"password": e.messages})



        password = make_password(validated_data["password"])
        user = User.objects.create(
            email=validated_data["email"],
            password=password,
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "state",
            "city",
            "bio",
            "age",
            "gender",
            "occupation",
            "marital_status",
            "language",
            "avater",
            "is_active",
        ]
        # fields = "__all__"


# user friend request serializers
class UserConnectorSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)  # Nested serializer for GET
    receiver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="receiver"
    )  # Use this for writable receiver during POST

    class Meta:
        model = UserConnector
        fields = ["id", "sender", "receiver", "receiver_id", "status"]


# reset password new to old password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
