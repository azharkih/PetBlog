from django.urls import path
from django.views.decorators.http import require_POST

from . import views

urlpatterns = [
    path('',
         views.index,
         name='index'),
    path('group/<slug:slug>/',
         views.group_posts,
         name='group_posts'),
    path('new/',
         views.NewPostView.as_view(),
         name='new_post'),
    path('follow/',
         views.FollowIndexView.as_view(),
         name='follow_index'),
    path('<str:username>/follow/',
         views.ProfileFollowView.as_view(),
         name='profile_follow'),
    path('<str:username>/unfollow/',
         views.ProfileUnfollowView.as_view(),
         name='profile_unfollow'),
    path('<str:username>/',
         views.UserProfileView.as_view(),
         name='profile'),
    path('<str:username>/<int:post_id>/',
         views.PostView.as_view(),
         name='post'),
    path('<str:username>/<int:post_id>/edit/',
         views.EditPostView.as_view(),
         name='post_edit'),
    path("<str:username>/<int:post_id>/comment/",
         require_POST(views.AddCommentView.as_view()),
         name='add_comment'),
]
