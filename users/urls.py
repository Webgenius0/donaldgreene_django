from django.urls import path, include
from .views import Home, SignupAPIView, UserProfileList, ChangePassword, ProfileList, ProfileDetail
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("home/", Home.as_view()),
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),



    path("user/profile/", UserProfileList.as_view(), name="user_profile_list"),
    path("profile/", ProfileList.as_view(), name="user_profile_list"),
    path("profile/<int:pk>/", ProfileDetail.as_view(), name="user_profile_detail"),
    # reset password by old password to new password
    path("change-password/<int:pk>/", ChangePassword.as_view(), name="change_password"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
