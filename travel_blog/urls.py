from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('posts.urls', namespace='travel_posts')),
    path('about/', include('about.urls', namespace='about')),
]

handler404 = 'core.views.page_not_found' # noqa
handler500 = 'core.views.server_error'  # noqa
handler403 = 'core.views.permission_denied' # noqa
