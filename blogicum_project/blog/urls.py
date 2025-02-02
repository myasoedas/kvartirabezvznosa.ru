# blogicum/blog/urls.py
from django.urls import path

from .views import (CategoryPostsListView, CommentDeleteView, rss_feed, robots_txt_view,
                    CommentUpdateView, IndexView, ListView, PostCommentView,
                    PostCreateView, PostDeleteView, PostDetailView,
                    PostEditView, UserProfileEditView, UserProfileView)
                    

app_name = 'blog'

urlpatterns = [
    path('category/<slug:category_slug>/', CategoryPostsListView.as_view(),
         name='category_posts'),
    path('profile/edit/', UserProfileEditView.as_view(), name='edit_profile'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='profile'),
    path('posts/list/', ListView.as_view(), name='posts_list'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', PostCreateView.as_view(), name='create_post'),
    path('posts/<int:post_id>/edit/', PostEditView.as_view(),
         name='edit_post'),
    path('posts/<int:post_id>/delete/', PostDeleteView.as_view(),
         name='delete_post'),
    path(
        'posts/<int:post_id>/comment/',
        PostCommentView.as_view(), name='add_comment'),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        CommentUpdateView.as_view(), name='edit_comment'),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        CommentDeleteView.as_view(), name='delete_comment'),
    path('rss-feed.xml', rss_feed, name='rss_feed'),
    path("robots.txt", robots_txt_view, name="robots_txt"),
    path('', IndexView.as_view(), name='index'),
]
