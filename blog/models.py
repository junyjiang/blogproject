from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):

    '''
    Django 要求数据库模型必须继承models.Model 类
    Django 就可以把这个类翻译成数据库的操作语言，在数据库里创建一个名为 category 的表格
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    当然 Django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
    Django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    '''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    """
        标签 Tag 也比较简单，和 Category 一样。
        再次强调一定要继承 models.Model 类！
    """
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

class Post(models.Model):

    # 文章标题
    title = models.CharField(max_length=70)
    # 文章正文
    # 存储比较短的字符串可以使用CharField类型但是储存较长的文本时我们需要使用TextField
    body = models.TextField()
    # 创建时间以及编辑时间
    # 存储创建时间以及最后编辑时间我们需要使用DateTimeField类型
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    # 文章摘要，可以没有文章摘要，但默认情况下CharField要求我们必须存入数据，否则会报错
    # 指定CharField 的blank属性为True，即：blank=True就可以为空了
    excerpt = models.CharField(max_length=200, blank=True)
    # 这是分类与标签，分类与标签的模型我们已经定义在上面
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微不同
    # 我们规定一篇文章只能关联一个分类，但是一个分类可以关联多篇文章，所以我们使用的是ForeignKey即一对的关联关系
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下面也可能有多个文章，所以我们使用ManyToManyField，多对多的关联关系】
    # 同时我们的文章可能会没有标签，所以标签tags要添加blank属性为True即：blank = True
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：https://docs.djangoproject.com/en/1.10/topics/db/models/#relationships
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tag, blank=True)
    # 文章作者，这里User是从diango.contrib.auth.models导入的
    # diango.auth.models是diango 内置的应用，专门用于处理用户注册、登录等流程，User是django为我们已经写好的用户模型
    # 这里我们使用ForeignKey 把文章和作者链接起来
    # 因为我们一篇文章只有一个作者，而一个作者可能会有多篇文章，因此我们使用的是一对多的关联关系类似Category
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.title
    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
