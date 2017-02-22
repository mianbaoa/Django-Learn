from django.shortcuts import render,redirect,get_object_or_404,render_to_response
from .forms import LoginForm,RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import NewUser,Post,PostType,PostTag
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
        context={'form':form,'post':post,'posttype':posttype,'posttags':posttags}
        return render(request,'post_page1.html',context)

def type_post(request,type_id):
    type=get_object_or_404(PostType,pk=type_id)
    posts=type.post_set.all()
    form=LoginForm()
    context = {'loginform': form, 'posts': posts, }
    return render(request,'index.html',context)

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



