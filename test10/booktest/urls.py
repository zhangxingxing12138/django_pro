from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include,url
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
schema_view=get_schema_view(title='Pastebin API')



router = DefaultRouter()
router.register(r'books',views.BookViewSet)
urlpatterns = [
    # url(r'^$',views.api_root),
    url('^', include(router.urls)),
    url(r'^schema/$',schema_view),
    url(r'^docs/',include_docs_urls(title='图书管理系统')),
    url(r'^publisher_list/$', views.publisher_list.as_view(),name='publisher-list'),
    url(r'^publishers/(?P<pk>[0-9]+)/$', views.publisher_detail.as_view(),name='publisher-detail'),
    # url(r'^books/$',book_list,name='book_list'),
    # url(r'^books/(?P<pk>[0-9])/$',book_detail,name='book_detail')
    #url(r'^books/$', views.BookList.as_view(),name='books_list'),
    #url(r'^books/(?P<pk>[0-9]+)/$', views.BookDetail.as_view(),name='books-detail')

]
