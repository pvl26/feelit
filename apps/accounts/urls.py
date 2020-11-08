from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile"),
    path('profile_update/', views.profile_update, name="profile_update"),
    path('create_profile/', views.create_profile, name="create_profile"),
    path('user_posts/?<username>', views.user_posts, name="user_posts"),
    path('user_posts/create_post/', views.create_post, name="create_post"),
    path('user_posts/read/?<id>', views.read, name="read")
]
