from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),


    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("deletefromwatchlist/<int:listing_id>", views.deletefromwatchlist, name="deletefromwatchlist"),
    path('mywatchlist', views.mywatchlist, name='mywatchlist'),

    path('close/<int:listing_id>', views.close, name='close'),

    path('bid/<int:listing_id>', views.bid, name='bid'),

    # categories
    path('categories/', views.categories, name='categories'),

    # category
    path('category/<int:category_id>', views.category, name='category'),

    # coment
    path('coment/<int:listing_id>', views.coment, name='coment'),
]
