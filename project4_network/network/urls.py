from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),

    # API Routes
    path("posts/", views.newpost, name="newpost"),
    path("likes/<str:post_id>", views.like, name="likes"),
    path("unlikes/<str:post_id>", views.unlike, name="unlikes"),
    path("edit/<str:post_id>", views.edit, name="edit"),
    path("follows/<str:user>", views.follow, name="follows"),
    path("unfollows/<str:user>", views.unfollow, name="unfollows"),
    path("posts/<str:posts>", views.posts, name="posts"),
    path("page/<str:posts>", views.page, name="page"),
]
