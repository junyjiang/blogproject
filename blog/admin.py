from django.contrib import admin
from .models import BlogType,Blog

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'typename')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'blogtype', 'author', 'created_time', 'last_updated_time')
