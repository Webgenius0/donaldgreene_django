from django.urls import path, include
from .views import Home, SignupAPIView, UserProfileList, UserProfileDetail,  ChangePassword, SigninView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("home/", Home.as_view()),
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("signin/", SigninView.as_view(), name="signin"),

    # path("signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),




    path("profile/", UserProfileList.as_view(), name="user_profile_list"),
    path("profile/<int:pk>/", UserProfileDetail.as_view(), name="user_profile_detail"),
    # reset password by old password to new password
    path("change-password/<int:pk>/", ChangePassword.as_view(), name="change_password"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
