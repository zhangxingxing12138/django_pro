import json
from .models import *
from django.db.migrations import serializer
from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import status
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Publisher
from django.http import HttpResponse
from . import serializers
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from booktest.permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from rest_framework import viewsets


# Create your views here.

# def publishers(request):
#     pub_list = Publisher.objects.all()
#
#     #第一种
#     list = []
#     for pub in pub_list:
#         d = {}
#         d['name'] = pub.name
#         d['address'] = pub.address
#         list.append(d)


     #第二种
    # for pub in pub_list:
    #     list.append(model_to_dict(pub))
    # return HttpResponse(json.dumps(list),content_type='application/json')


    #第三种
    # data = []
    # data = serializers.serialize('json', pub_list)
    # return HttpResponse(data, content_type='application/json')

    # p = Publisher.objects.all().first()
    # d = serializer.PublisherSerializers(p)
    # return HttpResponse(json.dumps(list(pub_list), content_type='application/json'))



# @api_view(['GET','POST'])
# def publisher_list(request):
#     if request.method == 'GET':
#         queryset = Publisher.objects.all()
#         s = serializers.PublisherSerializer(queryset, many=True)
#         return Response(s.data)
#     elif request.method == 'POST':
#         s = serializers.PublisherSerializer(data=request.data)
#         if s.is_valid():#检验数据是否正确
#             s.save()
#             return Response(s.data)
#         else:
#             return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
#
# from . import serializers
# @api_view(['GET','PuT','DELETE'])
# def publisher_detail(request,pk):
#     try:
#         p = Publisher.objects.get(pk=pk)
#     except p.DoesNotExist:
#         return Response(status.HTTP_204_NO_CONTENT)
#     if request.method == 'GET':
#         p = serializers.PublisherSerializer(p)
#         return Response(p.data)
#     elif request.method == 'PUT':
#         p = serializers.PublisherSerializer(p,data=request.data)
#         if p.is_valid():#检验数据是否正确
#             p.save()
#             return Response(p.data)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         p.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class publisher_list(APIView):
#
#     def get(self, request):
#         queryset = Publisher.objects.all()  # 查询出所有出版社
#         s = serializers.PublisherSerializer(queryset, many=True)#序列化
#         return Response(s.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         s = serializers.PublisherSerializer(data=request.data)
#         if s.is_valid():
#             s.save()
#             return Response(s.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
# class publisher_detail(APIView):
#     def get_object(self, pk):#重写objects
#         try:
#             return Publisher.objects.get(pk=pk)
#         except Publisher.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         publisher = self.get_object(pk)
#         s = serializers.PublisherSerializer(publisher)
#         return Response(s.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk, format=None):
#         publisher = self.get_object(pk)
#         s = serializers.PublisherSerializer(publisher, data=request.data)
#         if s.is_valid():
#             s.save()
#             return Response(s.data)
#         else:
#             Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         """删除出版社信息"""
#         publisher = self.get_object(pk)
#         publisher.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class publisher_list(mixins.ListModelMixin,
#                     mixins.CreateModelMixin,
#                     generics.GenericAPIView):
#     queryset = Publisher.objects.all()
#     serializer_class = serializers.PublisherSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
#
#
# class publisher_detail(mixins.RetrieveModelMixin,
#                       mixins.UpdateModelMixin,
#                       mixins.DestroyModelMixin,
#                       generics.GenericAPIView):
#
#     queryset = Publisher.objects.all()
#     serializer_class = serializers.PublisherSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

#最后的序列化
class publisher_list(generics.ListCreateAPIView):
    queryset = Publisher.objects.all()
    serializer_class = serializers.PublisherSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    #permissions.IsAuthenticated 不登录也可以访问
    def perform_create(self, serializer):
        serializer.save(operator=self.request.user)
class publisher_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Publisher.objects.all()
    serializer_class = serializers.PublisherSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
# 书籍的序列化

# class BookList(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = serializers.BookSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class BookDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = serializers.BookSerializer
#     permission_classes = (permissions.IsAuthenticated)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    permissions_classes = (permissions.IsAuthenticatedOrReadOnly)
# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response(
#         {
#             'publishers': reverse('publisher-list', request=request, format=format),
#             'books': reverse('books_list', request=request, format=format)
#         }
#     )