from django.contrib import admin

from .forms import BlogsForm
from .models import Blogs as BlogsModel


class BlogsAdmin(admin.ModelAdmin):
    list_display = ['user', '__str__', 'image']
    form = BlogsForm


admin.site.register(BlogsModel, BlogsAdmin)
