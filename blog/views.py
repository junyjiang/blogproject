import markdown
from django.shortcuts import render, get_object_or_404
from blog.models import Post


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
    # return render(request,'blog/index.html', context={'Title': 'ForTester首页', 'welcome': '欢迎访问ForTester首页'})
    # return HttpResponse("欢迎访问我的博客首页！")


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.toc',])
    return render(request, 'blog/detail.html', context={'post': post})


def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
