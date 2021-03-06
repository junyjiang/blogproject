from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from .models import Blog, BlogType




def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request,blogs_all_list)
    # context['blogs_count'] = Blog.objects.all().count()
    return render_to_response('blog/blog_list.html', context)

def blogs_with_type(request, blogtype_pk):

    blogtype = get_object_or_404(BlogType, pk=blogtype_pk)
    blogs_all_list = Blog.objects.filter(blogtype=blogtype)
    context = get_blog_list_common_data(request,blogs_all_list)
    context['blogtype'] = blogtype
    return render_to_response('blog/blogs_with_type.html', context)

def blogs_with_date(request, year, month):
    context={}
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request,blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render_to_response('blog/blogs_with_date.html', context)

def blog_detail(request, blog_pk):
    content = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    content['blog'] = blog
    content['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    content['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    return render_to_response('blog/blog_detail.html', content)

def get_blog_list_common_data(request,blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER) # 每页10篇进行分页
    page_num = request.GET.get('page', 1) # 通过get请求获取页码参数
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number # 获取当前页码
    # 获取当前页码前后各两页的页码范围
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] -1 >= 2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        blog_count = page_range.append(paginator.num_pages)
    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    # 获取博客每个分类的博客数量
    # BlogType.objects.annotate(blog_count=Count('blog'))
    #两者作用相同，但是上方的是再用到时才执行然后放置到内存中，下方是直接执行占用内存
    '''
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blogtype=blog_type).count()
        blog_types_list.append(blog_type)
    '''

    context={}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    # annotate作为注释blog_count会作为blog_types的属性
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return context