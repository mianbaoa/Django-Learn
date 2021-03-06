# -*- coding:utf-8 -*-
#这个类来扩充字段，之所以不自己写User模块，是因为内置的User模块使整个用户验证系统非常容易实现，
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
class NewUser(AbstractUser):

    profile=models.CharField(default="", max_length=256)
    name = models.CharField(default="", max_length=10)
    location = models.CharField(default="", max_length=10)

    def reply_me(self):
        comments=self.comment_set.all()
        return Reply_Comment.objects.filter(replied_comment__in=comments).order_by('-pub_date')

    def __str__(self):
        return self.username

class PostType(models.Model):
    name = models.CharField(max_length=10)
    intro = models.TextField(default='')

    def __str__(self):
        return self.name

class PostTag(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField('标题',max_length=20,default='')
    posttype = models.ForeignKey(PostType,null=True,blank=True,verbose_name='belong to')
    posttag = models.ManyToManyField('PostTag',verbose_name='标签')
    content = models.TextField('内容',default='')
    author = models.CharField('作者',default='',max_length=20)
    user = models.ManyToManyField('NewUser')#点赞收藏,多对多关系
    pub_date = models.DateTimeField('date published',default=timezone.now)
    update_time = models.DateTimeField(auto_now=True,null=True)
    published = models.BooleanField('notDraft',default=True)
    poll_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    keep_num = models.IntegerField(default=0)#收藏

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'post'

class Comment(models.Model):
    user = models.ForeignKey(NewUser,null=True)
    post = models.ForeignKey(Post,null=True)
    content = models.TextField(default='')
    pub_date = models.DateTimeField('date published',default=timezone.now)
    poll_num = models.IntegerField(default=0)
    reply_comment_num = models.IntegerField(default=0)

    def __str__(self):
        return self.content

class Reply_Comment(models.Model):

    user = models.ForeignKey(NewUser,null=True)
    replied_comment =models.ForeignKey(Comment,null=True)
    content = models.TextField(default='')
    pub_date = models.DateTimeField('date published',default=timezone.now)

    def __str__(self):
        return self.content

class Poll(models.Model):
    user=models.ForeignKey(NewUser,null=True)
    post=models.ForeignKey(Post,null=True)
    comment= models.ForeignKey(Comment,null=True)




