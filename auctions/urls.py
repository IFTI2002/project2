from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:list_id>", views.listing, name="listing"),
    path("category/<int:category_id>", views.category, name="category"),
    path("close", views.close, name="close"),
    path("remove", views.remove, name="remove"),
    path("comment/<int:list_id>", views.comment, name="comment")
]
