from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
def index(request):
    # return HttpResponse('视图函数')
    list=BookInfo.objects.all()
    ctx={
        'list':list,

    }
    return render(request,'booktest/index.html',ctx)
def show1(request):
    str=request.path
    str1=request.encoding
    method=request.method
    ctx = {

        'path': str,
        'encoding':str1,
        'method':method

    }
    return render(request,'booktest/show1.html',ctx)
def gettest(request):
    # if request.method=='GET'
    name=request.GET.get('name')
    # age=request.GET.get('age',20) 只能得到一个年龄，就是最后定义的年龄
    age = request.GET.getlist('age', 20)

    ctx={
        'name':name,
        'age':age
    }
    return render(request, 'booktest/showget.html', ctx)
def posttest(request):
    name=request.POST.get('name')
    gender=request.POST.get('gender','男')
    hobby=request.POST.getlist('hobby')
    ctx={
        'name':name,
        'gender':gender,
        'hobby':hobby,
    }
    return render(request, 'booktest/showpost.html', ctx)
def set_cookie(request):
    response=render(request,'booktest/set_cookie.html')
    response.set_cookie('name','laowang')
    response.set_cookie('age', 12,20)

    return response
def get_cookie(request):
    str=request.COOKIES.get('name')
    age = request.COOKIES.get('age')
    ctx={
        'str':str,
        'age':age,
    }

    return render(request,'booktest/getcookie.html',ctx)
def del_cookie(request):
    response=HttpResponse('删除成功')
    response.delete_cookie('name')
    return response
# Create your views here.
#去登陆
# 去登陆
def loginshow(request):
    name = request.session.get('myname', '去登陆')
    islogin = request.session.get('islogin', False)
    ctx = {
        'name': name,
        'islogin': islogin
    }
    return render(request, 'booktest/showlogin.html', ctx)
# 输入名字
def login(request):
    return render(request, 'booktest/login.html')
# 获取名字 存session 重定向去登陆页面
def loginhandle(request):
    name = request.POST.get('name')
    request.session['myname'] = name
    request.session['islogin'] = True
    request.session.set_expiry(0)  # 浏览器关闭就过期
    return HttpResponseRedirect('/loginshow/')
def loginout(request):
    del request.session['myname']
    del request.session['islogin']
    return HttpResponseRedirect('/loginshow/')