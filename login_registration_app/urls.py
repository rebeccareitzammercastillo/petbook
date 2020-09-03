from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('newaccount', views.newaccount),
    path('newsfeed', views.newsfeed),
    path('logout', views.logout),
    path('login', views.login),
    path('postmessage', views.postmessage),
    path('postcomment/<messageid>', views.postcomment)      
]