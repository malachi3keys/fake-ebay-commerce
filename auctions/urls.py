from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("tags/<str:tag_name>", views.tags, name="tags"),
    path("new", views.new, name="new"),
    path("<int:list_id>", views.list_item, name="list_item"),
    path("<int:list_id>/edit", views.edit, name="edit"),
]
