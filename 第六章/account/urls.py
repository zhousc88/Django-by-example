from django.conf.urls import url
from . import views
from django.contrib.auth.views import  login,logout,logout_then_login,password_change_done,password_change
from django.contrib.auth.views import  password_reset,password_reset_done,password_reset_confirm,password_reset_complete
app_name='account'

urlpatterns=[
    #url(r'^login/$',views.user_login,name='login'),
    url(r'^login/$',login,name='login'),
    url(r'^logout/$',logout,name='logout'),
    url(r'^logout-then-login/$',logout_then_login,
        name='logout_then_login'),
    url(r'^$',views.dashboard,name='dashboard'),
    url(r'^password-change/$',password_change,
        {'post_change_redirect': 'account:password_change_done'},
        name='password_change'),
    url(r'^password-change/done/$',password_change_done,name='password_change_done'),
    url(r'^password-reset/$',password_reset,{'post_reset_redirect': 'account:password_reset_done'},
        name='password_reset'),
    url(r'^password-reset/done/$',password_reset_done,name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',password_reset_confirm,
        {'post_reset_redirect':'account:password_reset_complete'}, name='password_reset_confirm'),
    url(r'^password-reset/complete/$',password_reset_complete,name='password_reset_complete'),
    url(r'^register/$',views.register,name='register'),
    url(r'^edit/$',views.edit,name='edit'),
    url(r'^users/$',views.user_list,name='user_list'),
    url(r'^users/(?P<username>[-\w]+)/$',views.user_detail,name='user_detail'),
    url(r'users/follow/$',views.user_follow,name='user_follow')
]