from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:pk>', views.profile, name='profile'),
    path('profiles', views.profiles, name='profiles'),
    path('account', views.account, name='account'),
    path('inbox', views.inbox, name='inbox'),
    path('message/<str:pk>', views.message, name='message'),
    path('send-message/<str:pk>', views.sendMessage, name='send-message'),
    path('edit-profile', views.updateAccount, name='edit-profile'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
    path('register', views.registerPage, name='register'),
    path('create-skill', views.createSkill, name='create-skill'),
    path('update-skill/<str:pk>', views.updateSkill, name='update-skill'),
    path('delete-skill/<str:pk>', views.deleteSkill, name='delete-skill'),
]
