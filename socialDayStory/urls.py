from django.urls import path
from .views import DayStoryList, DayStoryDetail, DayStoryLikeList, DayStoryCommentList, DayStoryShareList


urlpatterns = [
    path("stories/", DayStoryList.as_view(), name="day-story-list"),
    path("stories/<int:pk>/", DayStoryDetail.as_view(), name="day-story-detail"),
    path("stories/<int:pk>/likes/", DayStoryLikeList.as_view(), name="day-story-like-list"),
    path("stories/<int:pk>/comments/", DayStoryCommentList.as_view(), name="day-story-comment-list"),
    path("stories/<int:pk>/shares/", DayStoryShareList.as_view(), name="day-story-share-list"),


    # path("stories/<int:pk>/comments/", views.CommentList.as_view(), name="comment-list"),
    # path("stories/<int:pk>/likes/", views.LikeList.as_view(), name="like-list"),
    # path("stories/<int:pk>/shares/", views.ShareList.as_view(), name="share-list"),
    # path("stories/<int:pk>/comments/<int:comment_pk>/", views.CommentDetail.as_view(), name="comment-detail"),
    # path("stories/<int:pk>/likes/<int:like_pk>/", views.LikeDetail.as_view(), name="like-detail"),

]
