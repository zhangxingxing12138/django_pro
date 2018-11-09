from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^$',views.index),
    url(r'showtest/$',views.show1),
    url(r'gettest/$',views.gettest),
    url(r'posttest/$',views.posttest),
    url(r'set_cookie/$',views.set_cookie),
    url(r'get_cookie/$',views.get_cookie),
    url(r'del_cookie/$',views.del_cookie),
    url(r'^login/$', views.login),
    url(r'^loginshow/$', views.loginshow),
    url(r'^login_handle/$', views.loginhandle),
    url(r'^login_out/$', views.loginout),
]