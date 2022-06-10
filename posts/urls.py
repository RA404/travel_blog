from django.urls import path
from . import views


app_name = 'travel_posts'

urlpatterns = [
    path('', views.index, name='main'),
    path('country/<slug:slug>/', views.country_posts, name='country_posts'),
    path('profile/<str:user_name>', views.profile, name='profile'),
    path('post/<int:post_id>', views.post_detail, name='post_detail'),
]
