from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^create/$', views.create),
    url(r'^delete(\d+)/$',views.delete),
    url(r'^show/$', views.show),
    url(r'^zhuanyi/$',views.zhuanyi),

]