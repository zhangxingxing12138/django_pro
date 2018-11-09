from django.shortcuts import render,redirect
from .models import *
from datetime import date
def index(request):
    list=BookInfo.objects.all()
    ctx={
        'list':list
    }
    return render(request,'booktest/index.html',ctx)
def create(request):
    book=BookInfo()
    book.btitle = '流星蝴蝶剑'
    book.bpub_date = date(1995,12,30)
    book.save()
    return redirect('/')
def delete(request,id):
    book=BookInfo.objects.filter(id=int(id))
    book.delete()
    return redirect('/')


def show(request):
    # list = BookInfo.objects.filter(btitle__contains='笑')
    # list=BookInfo.objects.filter(btitle__endswith='部')
    # list=BookInfo.objects.filter(btitle__isnull=False)
    # list = BookInfo.objects.filter(id__in=[14,15])
    # list = BookInfo.objects.filter(id__gt=15)
    # list = BookInfo.objects.exclude(id=21)
    list = BookInfo.objects.filter(bpub_date__gt=date(1990,1,1))
    ctx = {
        'list': list
        # 'count':count
    }
    return render(request, 'booktest/show.html',ctx)
def zhuanyi(request):
    content='<h1>hello</h1>'
    ctx={
        'content':content,
    }
    return render(request,'booktest/zhuanyi.html',ctx)
# Create your views here.
