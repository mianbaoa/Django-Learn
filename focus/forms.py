# -*- coding:utf-8 -*-
from django import forms
from .models import PostType,PostTag
class LoginForm(forms.Form):
    uid=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'uid','placeholder':'Username'}))
    pwd=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form_control','id':'pwd','placeholder':'Password'}))

class RegisterForm(forms.Form):
    username=forms.CharField(label='username', max_length=100,
                             widget=forms.TextInput(attrs={'id':'username','onblur':'authentication()'}))
    email=forms.EmailField()
    password1=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(widget=forms.PasswordInput)

class CommentForm(forms.Form):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': '60', 'rows': '6'}))

class ProfileForm(forms.Form):
    name = forms.CharField(label='真实姓名',max_length=10)
    location = forms.CharField(label='家庭住址',max_length=10)
    profile = forms.CharField(label='自我介绍',widget=forms.Textarea(attrs={'cols': '60', 'rows': '6'}))


class PostTypeForm(forms.Form):
    posttypes = PostType.objects.all()
    TYPE_CHOICES = (
        (posttype.name,posttype.name) for posttype in posttypes
    )
    posttags = PostTag.objects.all()
    TAG_CHOICES = (
        (posttag.name,posttag.name) for posttag in posttags
    )
    post_type = forms.ChoiceField(label='post_type',choices=TYPE_CHOICES)
    post_tags = forms.MultipleChoiceField(label=u'文章标签',choices=TAG_CHOICES,widget=forms.CheckboxSelectMultiple())
    #这两个字段都是选择字段,选择文章类型