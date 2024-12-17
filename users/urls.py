from django.urls import path, include
from .views import (
    Home,
    SignupAPIView,
    AllUserProfileList,
    UserProfileList,
    UserProfileDetail,
    ChangePassword,
    SigninView,
    UserConnectorList,
    UserConnectorDetail,
)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("home/", Home.as_view()),
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("signin/", SigninView.as_view(), name="signin"),
    # path("signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # user profile list and detail
    path("profiles/", AllUserProfileList.as_view(), name="all_user_profiles"),

    # user profile list and detail by authenticated user id (current user)
    # path("profile/", UserProfileList.as_view(), name="user_profile_list"),
    # path("profile/<int:pk>/", UserProfileDetail.as_view(), name="user_profile_detail"),
    path("profile/", UserProfileList.as_view(), name="user_profile_list"),
    path("profile/<int:pk>/", UserProfileDetail.as_view(), name="user_profile_detail"),
    # user friend request list
    path("user-connector/", UserConnectorList.as_view(), name="user_connector_list"),
    path("user-connector/<int:pk>/", UserConnectorDetail.as_view(), name="user_connector_detail"),


    # reset password by old password to new password
    path("change-password/<int:pk>/", ChangePassword.as_view(), name="change_password"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
