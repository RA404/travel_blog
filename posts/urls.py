from django.urls import path
from . import views


app_name = 'travel_posts'

urlpatterns = [
    path('', views.index, name='main'),
    path('country/<slug:slug>/', views.country_posts, name='country_posts'),
    path('profile/<str:user_name>', views.profile, name='profile'),
    path('post/<int:post_id>', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
]
