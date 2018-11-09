from django.shortcuts import render
from .models import *
from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO
from django.http import HttpResponse
from django.shortcuts import  redirect
from django.shortcuts import  HttpResponseRedirect
from django.core.urlresolvers import reverse


# 变量
def index(request):
    b = BookInfo.objects.get(id=16)
    ctx = {
        'b': b,
    }
    return render(request, 'booktest/index.html', ctx)


# 段落
def index2(request):
    list = BookInfo.objects.all()
    # list=None
    ctx = {
        'list': list,
    }
    return render(request, 'booktest/index2.html', ctx)


# 过滤器
def index3(request):
    list = BookInfo.objects.all()
    ctx = {
        'list': list,
        'data': '隔壁老王',
    }
    return render(request, 'booktest/index3.html', ctx)


# 三层填坑
def index4(request):
    return render(request, 'booktest/index4.html')


def index5(request):
    return render(request, 'booktest/index5.html')


def user1(request):
    return render(request, 'booktest/user1.html')


def user2(request):
    return render(request, 'booktest/user2.html')


# csrf
def csrf1(request):
    return render(request,'booktest/csrf1.html')


def csrf2(request):
    name = request.POST.get('name')

    ctx = {
        'name': name
    }
    return render(request,'booktest/csrf2.html', ctx)
def login(request):
    return render(request,'booktest/login.html')
def login_check(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    if username=='smart' and password=='123':
        request.session['username']=username
        request.session['islogin'] =True
        return redirect('/post')
    else:
        return redirect('/login/')
def post(request):
    return render(request,'booktest/post.html')
def post_action(request):
    if request.session['islogin']:
        username=request.session['username']
        return HttpResponse('用户'+username+'发了一篇帖子')
    else:
        return HttpResponse('发帖失败')
# Create your views here.


#验证码

def verify_code(request):
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    buf = BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
def index7(request):
    return render(request,'booktest/index7.html')
def check_code(request):
    code=request.POST.get('code').lower()
    code1=request.session.get('verifycode').lower()
    if code== code1:
        return HttpResponse('成功')
    else:
        return HttpResponse('失败')
    # return render(request,'booktest/check_code.html',ctx)


def index6(request):
    ctx={
        'ctx':'<h1>哈哈</h1>'
    }
    return render(request, 'booktest/index6.html', ctx)

#反向解析
def fan1(request):
    return render(request, 'booktest/fan1.html')
def fan2(request):
    return HttpResponse('fan2')
def fan3(request,a,b):
    return HttpResponse(a+b)
def fan4(request,id,age):
    return HttpResponse(id+age)

#重定向
def fan5(request):
    return redirect(reverse('booktest:fan2'))

#静态文件
def index9(request):
    return render(request,'booktest/index9.html')
#中间件
def index10(request):
    # print(a)
    return render(request,'booktest/index10.html')
    # print('长相草你个')
#上传图片
def pic_upload(request):
    return render(request,'booktest/pic_upload.html')
from django.conf import settings
from django.http import HttpResponse

def pic_handle(request):
    f1=request.FILES.get('pic')
    fname='%s/booktest/%s'%(settings.MEDIA_ROOT,f1.name)
    with open(fname,'wb') as pic:
        for c in f1.chunks():
            pic.write(c)

    return HttpResponse('<img  src=/static/media/booktest/%s>'%(f1.name))

