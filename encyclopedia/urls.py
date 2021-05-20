from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name='create'),
    path("edit/<str:title>", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("random_page", views.random_page, name="random_page"),
    path("<str:title>", views.get_entry, name="get_entry"),
]

