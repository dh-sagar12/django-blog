from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path("signup/", views.SignUp, name="signup"),
    path('profile/edit/', views.EditProfile, name='edit_profile'),
    path("password/send-email/", views.SendForgetPasswordEmail, name="forgotPassword"),
    path("password/reset/<str:token>/", views.ResetPassword, name="reset_password"), 

]