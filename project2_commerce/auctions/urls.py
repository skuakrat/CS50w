from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category", views.category, name="category"),
    path("category/<int:category_id>", views.catview, name="catview"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("item/<int:item_id>", views.item, name="item"),
    path("bid/<int:item_id>", views.bid, name="bid"),
    path("close/<int:item_id>", views.close, name="close"),
    path("create", views.create, name="create"),
    path("comment/<int:item_id>", views.comment, name="comment"),
    path("watch/<int:item_id>", views.watch, name="watch"),
    path("unwatch/<int:item_id>", views.unwatch, name="unwatch"),
]
