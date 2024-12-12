from django.urls import path
from .views import SocialPostList, SocialPostDetail

urlpatterns = [
    path('socialPost/', SocialPostList.as_view(), name='social_post_list'),
    path('socialPost/<int:pk>/', SocialPostDetail.as_view(), name='social_post_detail'),  # Update the URL to include the primary key of the post.
    
]
