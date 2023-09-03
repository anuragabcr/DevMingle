from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:pk>', views.profile, name='profile'),
    path('profiles', views.profiles, name='profiles'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
    path('register', views.registerPage, name='register'),
]
