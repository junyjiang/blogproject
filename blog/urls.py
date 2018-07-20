from django.urls import path
from . import views

#start with blog 以blog开头
urlpatterns =[
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('type/<int:blogtype_pk>', views.blogs_with_type, name='blogs_with_type'),
]