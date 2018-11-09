from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index2$', views.index2),
    url(r'^index3$', views.index3),
    url(r'^index4$', views.index4),
    url(r'^index5$', views.index5),
    url(r'^user1$', views.user1),
    url(r'^user2$', views.user2),
    url(r'^csrf1$', views.csrf1),
    url(r'^csrf2/$', views.csrf2),
    url(r'^login/$', views.login),
    url(r'^login_check/$', views.login_check),
    url(r'^post/$', views.post),
    url(r'^post_action/$', views.post_action),


    url(r'^verify_code/$', views.verify_code),
    url(r'^index7/$', views.index7),
    url(r'^check_code/$', views.check_code),
    url(r'^index6/', views.index6),
    url(r'^fan1/', views.fan1),
    url(r'^fan2/', views.fan2, name='fan2'),
    url(r'^fan(\d+)_(\d+)/', views.fan3, name='fan2'),
    url(r'^fan(?P<id>\d+)_(?P<age>\d+)/$', views.fan4, name='fan2'),
    url(r'^fan5/', views.fan5),
    url(r'^index9/', views.index9),
    url(r'^index10/', views.index10),
    url(r'^pic_upload/$', views.pic_upload),
    url(r'^pic_handle/$', views.pic_handle),

]
