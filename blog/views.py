from django.shortcuts import render_to_response, get_object_or_404
from .models import Blog, BlogType


def blog_list(request):
    context={}
    context['blogs'] = Blog.objects.all()
    context['blog_types'] = BlogType.objects.all()
    context['blogs_count'] = Blog.objects.all().count()
    return render_to_response('blog/blog_list.html', context)

def blog_detail(request, blog_pk):
    content = {}
    content['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render_to_response('blog/blog_detail.html', content)

def blogs_with_type(request, blogtype_pk):
    context={}
    blogtype = get_object_or_404(BlogType, pk=blogtype_pk)
    context['blogs'] = Blog.objects.filter(blogtype=blogtype)
    context['blogtype'] = blogtype
    return render_to_response('blog/blogs_with_type.html', context)

