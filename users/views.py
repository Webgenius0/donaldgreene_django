from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .serializers import (
    SignupSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
)
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import Http404

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


class SigninView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            nullChecker = False
            serializer.is_valid(raise_exception=True)
            token_data = serializer.validated_data
            user = serializer.user
            if user.first_name == None:
                nullChecker = False
            else:
                nullChecker = True
            print(user.first_name)

            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "User signed in successfully.",
                    "user_id": user.id,
                    "user_email": user.email,
                    "is_profile": nullChecker,
                    "data": token_data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "status": 400,
                    "success": False,
                    "message": "Sign-in failed. Invalid credentials.",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserProfileList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = User.objects.filter(id=request.user.id)
        serializer = UserProfileSerializer(user, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "user profile get successful",
            "data": serializer.data,
        }
        return Response(response_data)

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "user profile created successful",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserProfileSerializer(user)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "user profile get successful",
            "data": serializer.data,
        }
        return Response(response_data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "user profile updated successful",
                "data": serializer.data,
            }
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



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
            obj = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if not obj.check_password(old_password):
            return Response({"error": "Old password does not match"}, status=400)

        obj.set_password(new_password)
        obj.save()
        return Response({"success": "Password changed successfully"}, status=200)


def login(request):
    return render(request, "users/login.html")
