
from django.urls import path

from . import views

urlpatterns = [
    path("posts", views.index, name="index"),
    path("add", views.add_view, name="add"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post/<str:id>", views.post, name="post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("mail/<str:type>", views.dm, name="dm"),
    path("new", views.new_mail, name="new_mail"),
    path("read/<str:dm_id>", views.read, name="read"),
    path("message/<str:name>", views.message, name="message"),
    path("", views.home, name="home"),
    path("post/activate/<str:post_id>", views.activate, name="activate"),
    path("post/deactivate/<str:post_id>", views.deactivate, name="deactivate"),
    path("fav/<str:post_id>", views.fav, name="fav"),
    path("unfav/<str:post_id>", views.unfav, name="unfav"),
    path("post/fav/<str:post_id>", views.fav, name="fav-post"),
    path("post/unfav/<str:post_id>", views.unfav, name="unfav-post"),
    path("update_image", views.update_image, name="update_image"),

]
