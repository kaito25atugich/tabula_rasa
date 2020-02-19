import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from markdownx.models import MarkdownxField



class User(AbstractUser):
    pass


class Introduction(models.Model):
    in_id = models.IntegerField(unique=True)
    introduction = models.TextField()

    def __str__(self):
        return 'ID :' + str(self.in_id) + self.introduction

class Category(models.Model):
    kind = models.CharField(verbose_name='カテゴリー', max_length=25)

    def __str__(self):
        return self.kind


class Post(models.Model):
    post = models.CharField(verbose_name='タイトル', max_length=100)
    category = models.ManyToManyField(Category, verbose_name='カテゴリー')
    content = MarkdownxField(verbose_name='コンテンツ')
    img = models.ImageField(verbose_name='画像', blank=True)
    created_at = models.DateTimeField(verbose_name='作成日', default=datetime.datetime.now())
    updated_at = models.DateTimeField(verbose_name='更新日', null=True, blank=True, default=datetime.datetime.now())
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.post


class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name='投稿',on_delete=models.CASCADE, blank=True, null=True)
    reply_to_me = models.ForeignKey('self', verbose_name='返信先', on_delete=models.CASCADE, blank=True, null=True)
    content = MarkdownxField(verbose_name='コメント', max_length=250)
    name = models.CharField(verbose_name='名前', max_length=25, default='名無し')
    created_at = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.content
