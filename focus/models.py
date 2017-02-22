
#这个类来扩充字段，之所以不自己写User模块，是因为内置的User模块使整个用户验证系统非常容易实现，
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
class NewUser(AbstractUser):

    profile=models.CharField(default="", max_length=256)

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
    pass




