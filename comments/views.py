from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .forms import CommentForm


def post_comment(request, post_pk):
    '''
    先获取被评论的文章，因为后续我们需要把评论和文章关联起来
    这里使用的get_object_or_404是为了防止我们获取的文章(Post)不存在时自动跳转到404页面
    若文章存在则获取文章
    '''
    post = get_object_or_404(Post, pk=post_pk)
    # HTTP请求由GET和POST两种，一般通过表单提交数据都是通过POST请求
    # 因此只有当用户的请求为 post 时才需要处理表单数据。
    if request.method == 'POST':
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象。
        # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了
        form = CommentForm(request.POST)
        # 当调用form.is_valid方法时，Django会帮我们检查表单的数据是否符合格式要求
        if form.is_valid():
            # 检测到表单提交的数据是合法的后我们使用save方法保存到数据库
            # commit=False 的作用仅仅利用表单的数据生成Comment 模型中的实例，但还不保存评论到数据库
            comment = form.save(commit=False)
            # 将评论同被评论的文章关联起来
            comment.post = post
            # 关联完成后将评论保存到数据库，调用模型实例的save方法
            comment.save()
            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)
        else:
            # 当我们检测到数据不合法后，重新渲染详情页面，并渲染表单的错误
            # 因此我们传递了三个变量给detail.html
            # 一个是文章（post），一个是表单（form），一个是评论列表（comment_list)
            # 注意我们这里使用了post.comment_set.all()方法，其作用是获取当前文章下的所有评论，类似Post.object.all()
            # 因为Post和Comment是ForeignKey(外键)关联的，因此使用post.comment_set.all()反向查询全部评论
            comment_list = post.comment_set.all()
            context = {'post': post, 'form': form, 'comment_list': comment_list}
            return render(request, 'blog/detail.html', context=context)
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    return redirect(post)
