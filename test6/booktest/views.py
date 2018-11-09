from django.shortcuts import render
from .models import *
from django.http import HttpResponse
import time
from django.conf import settings
from django.core.mail import send_mail
from . import tasks
#富文本
def goods(request):
    list=GoodsInfo.objects.all()
    ctx={
        'list':list,
    }
    return render(request,'booktest/goods.html',ctx)
def editor(request):
    return render(request, 'booktest/editor.html')
#上传到数据库
def submit_x(request):
    p = request.POST.get('gcontent')
    g=GoodsInfo()
    g.gcontent=p
    g.save()
    return HttpResponse('ok')

#全文搜索
def query(request):
    return render(request,'booktest/query.html')

#celery

def sayhello(request):
# print('hello ...')
# time.sleep(2)
# print('world ...')
    tasks.sayhello.delay()
    return HttpResponse("hello world")

#163发送邮件

def send(request):
    send.delay() 
    msg='<a href="#" target="_blank">点击激活</a>'
    send_mail('注册激活','',settings.EMAIL_FROM,
    ['15582304596@163.com'],
    html_message=msg)

    return HttpResponse('ok')


from django.views.decorators.cache import cache_page
# Create your views here.
@cache_page(60 * 15)
def index(request):
    return HttpResponse('hello1')
    #return HttpResponse('hello2')
def index2(request):
    return render(request,'booktest/index2.html')



