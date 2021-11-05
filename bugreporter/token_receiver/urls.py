from django.contrib import admin
from django.urls import path, include

from token_receiver import views

urlpatterns = [
    path('backend/gettoken', views.getToken.as_view({'get': 'get_token'}))
    ]