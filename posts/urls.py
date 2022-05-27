from django.urls import path
from . import views


app_name = 'travel_posts'

urlpatterns = [
    path('', views.index, name='main'),
    path('country/<slug:slug>/', views.country_posts, name='country_posts'),
]
