from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.api.urls')),
    path('api/blogs/', include(('blogs.api.urls', 'api-blogs'), namespace='api-blogs')),
    path('api/user/', include(('accounts.api.users.urls', 'api-user'), namespace='api-user'))
]
