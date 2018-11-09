from django.conf.urls import url
from . import views
urlpatterns = [
url(r'^goods$', views.goods),
url(r'^editor/$',views.editor),
url(r'^submit_x/$',views.submit_x),
url(r'^query/', views.query),
url(r'^sayhello$',views.sayhello),
url(r'^send/$',views.send),
url(r'^index/$',views.index),
url(r'^index2/$',views.index2),
]

