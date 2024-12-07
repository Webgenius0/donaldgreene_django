from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import CustomUser
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .serializers import (
    SignupSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
)
from rest_framework import generics


# Create your views here.


class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)


class SignupAPIView(APIView):

    permission_classes = []

    def post(self, request):
        password = request.POST.get("password", None)
        confirm_password = request.POST.get("confirm_password", None)
        if password == confirm_password:
            serializer = SignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            response = status.HTTP_201_CREATED
        else:
            data = ""
            raise ValidationError(
                {"password_mismatch": "Password fields didn not match."}
            )
        return Response(data, status=response)


class UserProfileList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = CustomUser.objects.filter(id=request.user.id)
        serializer = UserProfileSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# reset password by old password to new password
class ChangePassword(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        try:
            obj = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if not obj.check_password(old_password):
            return Response({"error": "Old password does not match"}, status=400)

        obj.set_password(new_password)
        obj.save()
        return Response({"success": "Password changed successfully"}, status=200)



def login(request):
    return render(request, 'users/login.html')