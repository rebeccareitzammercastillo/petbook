from django.urls import path     
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('newaccount', views.newaccount),
    path('newsfeed', views.newsfeed),
    path('profile/<profileid>', views.profile),
    path('logout', views.logout),
    path('login', views.login),
    path('postmessage', views.postmessage),
    path('postcomment/<messageid>', views.postcomment),    
    path('delete/<postid>', views.deletepost),
    path('deletecomment/<commentid>', views.deletecomment),
    path('profilemessage/<profileid>', views.profilemessage),
    path('profile/<profileid>/comment/<commentid>', views.profilecomment),    
    path('profile/<profileid>/deleteprofilepost/<postid>', views.deleteprofilepost),
    path('profile/<profileid>/deleteprofilecomment/<commentid>', views.deleteprofilecomment),
]