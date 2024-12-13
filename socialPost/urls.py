from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', views.PostLike.as_view(), name='post-like'),
    path('posts/<int:pk>/comment/', views.PostComment.as_view(), name='post-comment'),
    path('posts/<int:pk>/share/', views.PostShare.as_view(), name='post-share'),
    path('posts/<int:pk>/comments/', views.CommentList.as_view(), name='comment-list'),
    path('posts/<int:pk>/likes/', views.LikeList.as_view(), name='like-list'),
    path('posts/<int:pk>/shares/', views.ShareList.as_view(), name='share-list'),
]