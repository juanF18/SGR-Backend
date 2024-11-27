from django.urls import path
from . import views

urlpatterns = [
    path("comments/", views.CommentView.as_view(), name="comments_view"),
    path(
        "comments/<int:pk>/",
        views.CommentDetailView.as_view(),
        name="comment_detail_view",
    ),
    path(
        "comments/<int:user_id>/",
        views.CommentUserView.as_view(),
        name="user_comments_view",
    ),
]