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

    #Register
    path('register/', views.register, name="register"),
    
    #Edit User
    path('edit/', views.edit_user, name="edit_user"),

    #Ticket
    path('ticket', views.ticket, name="ticket"),

    #Change Password
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url='done/'), name= "password_change"),
    
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name= "password_change_done"),

    #Reset Password
    path('password-reset/', auth_views.PasswordResetView.as_view(success_url='done/'), name= "password_reset"),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name= "password_reset_done"),
    
    path('password-reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(\
        success_url='/password-reset/complete/'), name="password_reset_confirm"),
    
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(),\
        name="password_reset_complete"),

    #post list
    path('posts/', views.post_list, name="post_list"),

    #post list with tag
    path('posts/<tag_slug>/', views.post_list, name="post_list_by_tag"),

    #Create Post
    path('posts/create_post', views.create_post, name="create_post"),
]