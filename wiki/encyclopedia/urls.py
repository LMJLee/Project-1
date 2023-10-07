from django.urls import path

from . import views
from . import util

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search/", views.search, name="search"),
    path("createpage/", views.createpage, name="createpage")
]
