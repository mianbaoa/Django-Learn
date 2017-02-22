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
    url(r'^sub_post/$',views.sub_post,name='sub_post')
]