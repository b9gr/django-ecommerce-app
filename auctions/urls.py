from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:auction_id>", views.auction, name="auction"),
    path("createbid/<int:auction_id>", views.createBid, name="createBid"),
    path("makecomment/<int:auction_id>", views.makecomment, name="makecomment"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.spesificcategories, name="spesificcategories"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("create", views.create, name="create"),
    path("register", views.register, name="register")
]
