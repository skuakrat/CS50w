from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("edit", views.edit, name="edit"),
    path("wiki/", views.randompage, name="random"),
    path("wiki/edit", views.edit2, name="edit2"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.search, name="search"),
]
