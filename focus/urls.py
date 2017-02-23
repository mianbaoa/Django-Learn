from django.conf.urls import include,url
from . import views

urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^login/$',views.log_in,name='login'),
    url(r'^logout/$',views.log_out,name='logout'),
    url(r'^register/$',views.register,name='register'),
    url(r'^active/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$',views.token_confirm,name='token_confirm'),
    url(r'^post/(?P<post_id>\w+)/$',views.post_page,name='post_page'),
    url(r'^type_post/(?P<type_id>\w+)/$',views.type_post,name='type_post'),
    url(r'^add_post/$',views.add_post,name='add_post'),
    url(r'^sub_post/$',views.sub_post,name='sub_post'),
    url(r'^comment/(?P<post_id>\w+)/$',views.add_comment,name='add_comment'),
    url(r'^get_poll_post/(?P<post_id>\w+)/$',views.get_poll_post,name='get_poll_post'),
    url(r'^get_poll_comment/(?P<comment_id>\w+)/$',views.get_poll_comment,name='get_poll_comment'),
    url(r'^keep_post/(?P<post_id>\w+)/$',views.keep_post,name='keep_post'),
    url(r'^my_keep/$',views.my_keep,name='my_keep'),
    url(r'^comment_page/(?P<comment_id>\w+)/$',views.comment_page,name='comment_page'),
    url(r'^reply_comment/(?P<comment_id>\w+)/$',views.reply_comment,name='reply_comment'),
    url(r'^user/(?P<user_id>\w+)/$',views.user,name='user'),
    url(r'^add_profile/$',views.add_profile,name='add_profile'),
    url(r'^get_search/$',views.get_search,name='get_search')
]