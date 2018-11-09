from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.area),
    url(r'^area/$',views.area),
    url(r'^area1/$', views.area1),
    url(r'^area2/$', views.area2),
    url(r'^area3_(\d+)/$', views.area3),
    url(r'^page_text/(\d*)/$', views.page_text),
]