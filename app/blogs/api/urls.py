from django.urls import path

from .views import BlogsListView, BlogsDetailView

urlpatterns = [
    path('', BlogsListView.as_view()),
    path('<id>', BlogsDetailView.as_view(), name='details'),
]
