from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('country/<slug:slug>/', views.country_posts),
]
