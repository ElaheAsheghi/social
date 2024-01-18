from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'social'
urlpatterns = [
    #profile
    path('', views.profile, name="profile"),
    #Login
    path('login/', views.UserLoginView.as_view(), name="login"),
    #Logout
    path('logout/', views.Logout, name="logout"),
]