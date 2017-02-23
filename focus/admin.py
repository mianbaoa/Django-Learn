from django.contrib import admin
from django.db import models
from django import forms
from .models import Comment,Post,PostType,NewUser,PostTag,Reply_Comment
# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display=('user_id','post_id','pub_date','content','poll_num')


class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(
            attrs={'rows': 41,
                   'cols': 100
                   })},
    }
    list_display = ('title', 'pub_date', 'poll_num')


class NewUserAdmin(admin.ModelAdmin):
    list_display = ('username',)


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'intro')
class PosttagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile')

class ReplyCommentAdmin(admin.ModelAdmin):
    list_display = ('user_id','replied_comment_id','pub_date','content')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, ArticleAdmin)
admin.site.register(PostType, ColumnAdmin)
admin.site.register(PostTag,PosttagAdmin)
admin.site.register(NewUser, NewUserAdmin)
admin.site.register(Reply_Comment,ReplyCommentAdmin)
#admin.site.register(Author, AuthorAdmin)
