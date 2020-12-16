from django.urls import path
from . import views

urlpatterns = [
    path('main', views.index),
    path('reg', views.reg),
    path('signin', views.signin),
    path('create_user', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('main_lg', views.dashboard),
    path('market/<int:id>', views.market_info),
    path('user/<int:id>', views.profile),
    path('user/<int:id>/favorites', views.user_fav),
    path('item/<int:id>', views.item_info),
    path('item/<int:id>/add', views.add_to_fav),
    path('item/<int:id>/remove', views.remove_from_fav)

]