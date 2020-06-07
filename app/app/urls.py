from django.contrib import admin
from django.urls import path, include

#from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/auth/', obtain_jwt_token),
    # path('api/auth/refresh', refresh_jwt_token),
    path('api/auth/', include('accounts.api.urls')),
    path('api/blogs/', include(('blogs.api.urls', 'api-blogs'), namespace='api-blogs')),
    path('api/user/', include(('accounts.api.users.urls', 'api-user'), namespace='api-user'))
]
