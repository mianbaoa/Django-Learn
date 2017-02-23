from django.shortcuts import render,redirect,get_object_or_404,render_to_response
from .forms import LoginForm,RegisterForm,CommentForm,ProfileForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import NewUser,Post,PostType,PostTag,Comment,Poll,Reply_Comment
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .utils.token import Token
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.core.urlresolvers import reverse
# Create your views here.
#login 主页面
def index(request):
    loginform=LoginForm()
    posts=Post.objects.order_by('-pub_date')
    page = int(request.GET.get('page',1))
    posts_page = posts[(page-1)*5:page*5]
    context={'loginform':loginform,'posts':posts,'posts_page':posts_page}
    return render(request,'index.html',context)

def user(request,user_id):
    user=get_object_or_404(NewUser,pk=user_id)
    return render(request,'user.html',{'user':user})

def add_profile(request):
    user=request.user
    if request.method == 'GET':
        form=ProfileForm()
        return render(request, 'add_profile.html', {'form':form})
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            profile = form.cleaned_data['profile']
            location = form.cleaned_data['location']
            print('name:'+name)
            user.name = name
            user.profile = profile
            user.location = location
            user.save()
            messages.success(request,'个人资料修改成功！')
            return redirect('/focus/user/'+str(user.id))
def log_in(request):
    if request.method == 'GET':
        form=LoginForm()
        return render(request,'login.html',{'form':form})
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['uid']
            password=form.cleaned_data['pwd']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                url = request.POST.get('source_url','/focus')#得到POST里name='source_url'表单中的值，若没有source_url这一栏。给POST里的source_url赋值为/focus
                return redirect(url)
            else:
                messages.error(request,u'用户名或者密码错误！或者该用户未激活，请前往验证邮箱激活账户！')
                return render(request,'login.html',{'form':form})
        else:
            return render(request,'login.html',{'form':form})
@login_required
def log_out(request):
    url = request.POST.get('source_url','/focus')
    logout(request)
    return redirect(url)

def register(request):
    if request.method == 'GET':
        form=RegisterForm()
        return render(request, 'register.html', {'form':form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if request.POST.get('raw_username', 'erjgiqfv240hqp5668ej23foi') != 'erjgiqfv240hqp5668ej23foi': #if ajax
            try:
                user = NewUser.objects.get(username=request.POST.get('raw_username',''))
            except ObjectDoesNotExist:
                return render(request, 'register.html', {'form': form, 'msg': '该用户名可以使用'})
            else:
                return render(request, 'register.html', {'form': form, 'msg': '该用户名已存在'})
        else:
            if form.is_valid():
                a=form.cleaned_data
                username=a['username']
                email=a['email']
                password1=a['password1']
                password2=a['password2']
                if password1==password2:
                    user = NewUser(username=username,email=email,password=password1,is_active=False)
                    user.set_password(password1)
                    #在这加上这句话就把密码加密了！
                    user.save()
                    token_confirm=Token(settings.SECRET_KEY)
                    token=token_confirm.generate_validate_token(user.username)
                    message='\n'.join([u'欢迎{},加入到我的博客'.format(username),u'请访问链接，完成用户验证:',
                                       '/'.join([settings.DOMAIN, 'active',token])])
                    send_mail(u'验证用户信息', message, '18435151481@163.com', [email,], fail_silently=False)
                    messages.error(request,u'验证邮件已发送至邮箱，请登录到注册邮箱中验证用户，有效期为1个小时。')
                    return redirect(reverse('focus:login'))
                else:
                    return render(request, 'register.html', {'form':form, 'msg':'第二次输入密码不等于原密码!'})
            else:
                return render(request, 'register.html')

def token_confirm(request,token):
    token_confirm = Token(settings.SECRET_KEY)
    try:
        username=token_confirm.confirm_validate_token(token)
    except:
        username=token_confirm.remove_validate_token(token)
        users=NewUser.objects.filter(username=username)
        for user in users:
            user.delete()
        messages.error(request,u'用户验证令牌已过期，请重新注册')

        return redirect(reverse('focus:register'))
    try:
        user=NewUser.objects.get(username=username)
    except NewUser.DoesNotExist:
        messages.error(request,u'验证用户未找到，请重新注册')
        return redirect(reverse('focus:register'))
    if not user.is_active:
        user.is_active=True
        user.save()
        messages.success(request, u'验证成功，请登录！')
        return redirect(reverse('focus:login'))
    else:
        messages.error(request, u'请勿重复验证!')
        return redirect(reverse('focus:login'))

def post_page(request,post_id):
    if request.method=='GET':
        post=get_object_or_404(Post,pk=post_id)
        posttype=post.posttype
        posttags=post.posttag.all()
        form=LoginForm()
        commentform=CommentForm()
        comments=Comment.objects.filter(post=post)
        page = int(request.GET.get('page',1))
        comments_page = comments[(page-1)*5:page*5]
        context={'form':form,'post':post,'posttype':posttype,'posttags':posttags,
                 'commentform':commentform,'comments':comments,'comments_page':comments_page}
        return render(request,'post_page1.html',context)

def type_post(request,type_id):
    type=get_object_or_404(PostType,pk=type_id)
    posts=type.post_set.all()
    form=LoginForm()
    context = {'loginform': form, 'posts': posts, }
    return render(request,'some_post.html',context)

def add_post(request):
    return render(request,'add_post.html')

def sub_post(request):
    if request.method == 'GET':
        title = request.GET['post_title']
        type = request.GET['post_type']
        content = request.GET['post_content']
        tags = request.GET.getlist('post_tags')
        posttype=PostType.objects.filter(name=type).first()
        post = Post(title=title,content=content,author='苦咖啡',posttype=posttype)
        post.save()
        for tag in tags:
            post_tag = PostTag.objects.filter(name=tag).first()
            post.posttag.add(post_tag)
        messages.success(request,u'文章发表成功！！')
        return redirect(reverse('focus:index'))

@login_required
def add_comment(request,post_id):
    form=CommentForm(request.POST)
    post = Post.objects.get(pk=post_id)
    user = request.user
    url = '/focus/post/'+post_id
    if form.is_valid():
        content = form.cleaned_data['comment']
        comment=Comment(post=post,user=user,content=content)
        comment.save()
        post.comment_num +=1
        post.save()
        messages.success(request,'发表评论成功')
        return redirect(url)

@login_required
def get_poll_post(request,post_id):
    post=Post.objects.get(pk=post_id)
    logger_user = request.user
    polls=logger_user.poll_set.all()
    posts=[]
    for poll in polls:
        posts.append(poll.post)
    if post not in posts:
        poll=Poll(user=logger_user,post=post)
        post.poll_num+=1
        poll.save()
        post.save()
        return redirect('/focus/post/'+post_id)
    else:
        return redirect('/focus/post/'+post_id)
#明天研究session来用点赞

@login_required
def get_poll_comment(request,comment_id):
    comment=Comment.objects.filter(pk=comment_id).first()
    post=comment.post
    user = request.user
    polls=user.poll_set.all()
    comments=[]
    for poll in polls:
        comments.append(poll.comment)
    if comment in comments:
        return redirect('/focus/post/'+str(post.id))
    else:
        poll=Poll(user=user,comment=comment)
        poll.save()
        comment.poll_num+=1
        comment.save()
        return redirect('/focus/post/'+str(post.id))
@login_required
def keep_post(request,post_id):
    post=Post.objects.get(pk=post_id)
    user=request.user
    posts = user.post_set.all()
    if post not in posts:
        post.user.add(user)
        post.keep_num+=1
        post.save()
        request.session['has_keep']=True
        messages.success(request,u"文章已收藏，请到'我的收藏'中查看。")
        return redirect('/focus/post/'+post_id)
    else:
        messages.error(request,u'请勿重复收藏！')
        return redirect('/focus/post/'+post_id)

@login_required
def my_keep(request):
    user=request.user
    posts=user.post_set.all()
    return render(request,'some_post.html',{'posts':posts})

@login_required
def comment_page(request,comment_id):
    comment=Comment.objects.get(pk=comment_id)
    form=CommentForm()
    comments = Reply_Comment.objects.filter(replied_comment=comment)
    return render(request,'comment_page.html',{
        'comment':comment,
        'comments':comments,
        'form':form
    })

#回复别人
@login_required
def reply_comment(request,comment_id):
    user = request.user
    comment = Comment.objects.get(id=comment_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data['comment']
        reply_comment = Reply_Comment(content=content,user=user,replied_comment=comment)
        reply_comment.save()
        comment.reply_comment_num +=1
        post=comment.post
        post.comment_num+=1
        post.save()
        comment.save()
        messages.success(request,'回复成功！')
        return redirect('/focus/comment_page/'+comment_id)
#得到搜索的post
def get_search(request):
    key = request.POST['search_value']
    posts = Post.objects.all()
    Search_result = []
    for post in posts:
        if key in post.title:
            Search_result.append(post)
        elif key in post.content:
            Search_result.append(post)
    if len(Search_result) == 0:
        Search = 'Error'
    else:
        Search = 'Success'
    Search_count = len(Search_result)
    return render(request,'Search.html',{
        'Search_result':Search_result,
        'Search_count':Search_count,
        'Search':Search,
        'key':key
    })
#显示回复我的所有评论
def reply_me(request):
    user = request.user
    comments=user.reply_me
    return render(request,'reply_me.html',{'comments':comments})

