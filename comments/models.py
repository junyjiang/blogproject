from django.db import models


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    # 允许为空
    url = models.URLField(blank=True)
    # 大量字符使用TextField
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('blog.Post', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text[:20]