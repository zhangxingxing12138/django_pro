from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render

# from blog.userapp.models import *
from .models import *
from django.views.generic.base import View
from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from random import Random
from django.core.mail import send_mail

from django.http import HttpResponse
from userapp.models import BlogUser,EmailVerifyRecord
from blog.settings import EMAIL_FROM
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
import json
import datetime as dt

def index(request):
    banner_list = Banner.objects.all()
    recommend_list = Post.objects.filter(recommend=True).all()
    # all()后面加[:1]只显示一条
    post_list = Post.objects.order_by('-pub_date').all()[:10]  # 最新发布
    blogcategory_list = BlogCategory.objects.all()  # 分类
    comment_list = Comment.objects.order_by('-pub_date').all()  # 最新评论 -pub_date 表示倒序
    num = []  # 用来装id
    new_comment_list = []  # 用来装过滤后的评论
    for c in comment_list:
        if c.post.id not in num:
            num.append(c.post.id)
            new_comment_list.append(c)

    friendlylink_list = FriendlyLink.objects.all()  # 友情链接
    ctx = {
        'banner_list': banner_list,
        'recommend_list': recommend_list,
        'post_list': post_list,
        'blogcategory_list': blogcategory_list,
        'new_comment_list': new_comment_list,
        'friendlylink_list': friendlylink_list,
    }
    return render(request, 'booktest/index.html', ctx)


# 搜索条功能
def search(request):
    kw = request.GET.get('keyword', '')
    tags_list = Tags.objects.all()
    post_list = Post.objects.filter(Q(tags__name__icontains=kw) | Q(title__icontains=kw) | Q(content__icontains=kw))
    comment_list = Comment.objects.order_by('-pub_date').all()  # 最新评论 -pub_date 表示倒序

    num = []  # 用来装id
    new_comment_list = []  # 用来装过滤后的评论
    # if request.method == 'POST':

    for c in comment_list:
        if c.post.id not in num:
            num.append(c.post.id)
            new_comment_list.append(c)

    try:

        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(post_list, per_page=1, request=request)
    post_list = p.page(page)

    ctx = {
        'post_list': post_list,
        'tags_list': tags_list,
        'new_comment_list': new_comment_list,
    }
    return render(request, 'booktest/list.html', ctx)


class TagMessage(object):
    def __init__(self, tid, name, count):
        self.tid = tid
        self.name = name
        self.count = count


# 分页
def blog_list(request, cid=-1, tid=-1):
    post_list = None
    if cid != -1:
        cat = BlogCategory.objects.get(id=cid)
        post_list = cat.post_set.all()
    elif tid != -1:
        tag = Tags.objects.get(id=tid)
        post_list = tag.post_set.all()
    else:  # 不传分类或者标签id就找全部
        post_list = Post.objects.all()
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(post_list, per_page=1, request=request)
    post_list = p.page(page)
    tags = Tags.objects.all()
    tag_message_list = []
    for t in tags:
        count = len(t.post_set.all())
        tm = TagMessage(t.id, t.name, count)
        tag_message_list.append(tm)
    comment_list = Comment.objects.order_by('-pub_date').all()  # 最新评论 -pub_date 表示倒序
    num = []  # 用来装id
    new_comment_list = []  # 用来装过滤后的评论
    for c in comment_list:
        if c.post.id not in num:
            num.append(c.post.id)
            new_comment_list.append(c)

    ctx = {
        'post_list': post_list,
        'tags': tag_message_list,
        'new_comment_list': new_comment_list,

    }
    return render(request, 'booktest/list.html', ctx)


# 详情页
def blog_detail(request, bid):
    post = Post.objects.get(id=bid)
    post.views = post.views + 1
    post.save()
    comment_list = Comment.objects.order_by('-pub_date').all()  # 最新评论 -pub_date 表示倒序
    num = []  # 用来装id
    new_comment_list = []  # 用来装过滤后的评论
    comments_list = post.comment_set.all()
    for c in comment_list:
        if c.post.id not in num:
            num.append(c.post.id)
            new_comment_list.append(c)
    tag_list = post.tags.all()
    tag_post_list = []

    for tag in post.tags.all():
        tag_post_list.extend(tag.post_set.all())

    ctx = {
        'post': post,
        'new_comment_list': new_comment_list,
        'tag_post_list': tag_post_list,
        'comments_list': comments_list,
    }
    return render(request, 'booktest/show.html', ctx)

def CommentView(request, bid):
    comment = Comment()
    comment.user = request.user
    comment.post = Post.objects.get(id=bid)
    comment.content = request.POST.get('content')
    comment.pub_date = datetime.now()
    comment.save()
    return HttpResponseRedirect(reverse("blog_detail", kwargs={"bid": bid}))


# 登录

def loginin(request):
    if request.method == 'GET':
        return render(request, 'booktest/login.html')

    elif request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')

        # user = authenticate(username=uname, password=pwd)
        user = BlogUser.objects.filter(username=uname)
        if len(user) > 0:
            if user[0].is_active:
                if check_password(pwd, user[0].password):
                    login(request, user[0])
                    # #假如他没勾选自动登录
                    #     request.session.set_expiry(0)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, 'booktest/login.html', {"error_msg": '用户或密码错误'})
            else:
                return render(request, 'booktest/login.html', {"error_msg": '用户没激活'})
        else:
            return render(request, 'booktest/login.html', {"error_msg": '用户或密码错误'})


#注册
def register(request):
    if request.method == 'GET':
        return render(request, 'booktest/register.html')
    elif request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        email = request.POST.get('email')
        print(uname)
        user = BlogUser.objects.filter(username=uname)
        print(user)
        print(len(user))
        if len(user) > 0:
            return render(request, 'booktest/register.html', {"error_msg": "用户名已存在"})

        user = BlogUser.objects.filter(email=email)
        if len(user) > 0:
            return render(request, 'booktest/register.html', {"error_msg": "邮箱已存在"})
        my_send_email(email)  # task任务 耗时
        user = BlogUser()
        user.username = uname
        user.password = make_password(pwd)
        user.email = email
        user.is_active = False  # 没激活
        # user.is_staff #是否可以登录管理后台
        # user.is_superuser #是否是超管
        # user.is_authenticated #是否严重
        user.save()
        return render(request, 'booktest/login.html', {"error_msg": "已经向当前邮箱发送一封邮件"})





# 生成随机字符串
def make_random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 发送邮件
def my_send_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = make_random_str(4)
    else:
        code = make_random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "博客-注册激活链接"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "博客-网注册密码重置链接"
        email_body = "请点击下面的链接重置密码: http://127.0.0.1/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "update_email":
        email_title = "博客-邮箱修改验证码"
        email_body = "你的邮箱验证码为: {0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
#验证
class ActiveView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        #fliter返回可以遍历的列表
        #get返回的是对象，不能遍历
        if all_records:
            for record in all_records:
                email = record.email
                user = BlogUser.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return HttpResponse('验证失败')
        return render(request,"booktest/login.html")

def reset(request, active_code):
    all_records = EmailVerifyRecord.objects.filter(code=active_code)
    if all_records:
        for record in all_records:
            email = record.email
            request.session['email'] = email
            # record.delete()
            return render(request, 'booktest/newpwd.html')
    else:
        return HttpResponse("验证失败")
    return render(request, "login.html")
def forget(request):
    if request.method == 'GET':
        return render(request, "booktest/forpwd.html")
    else:
        email = request.POST.get('email')
        user = BlogUser.objects.filter(email=email)
        if len(user) == 0:
            return render(request, 'booktest/register.html', {"error_msg": "邮箱未注册"})
        else:
            my_send_email(email, send_type="forget")
            return render(request, 'booktest/forpwd.html', {"error_msg": "邮箱已发送"})
def newpwd(request):
    if request.method == 'POST':
        pwd1, pwd2 = request.POST.getlist('password')
        if pwd1 != pwd2:
            return render(request, "booktest/newpwd.html", {"error_msg": "密码不一样"})
        else:
            email = request.session.get('email')
            user = BlogUser.objects.get(email=email)
            user.set_password(pwd1)
            user.save()
            request.session.flush()

            return HttpResponseRedirect('/login/')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))



@csrf_exempt
def upload_image(request, dir_name):
    ################## #  kindeditor图片上传返回数据格式说明： # {"error": 1, "message": "出错信息"} # {"error": 0, "url": "图片地址"} ################## result = {"error": 1, "message": "上传出错"}
    files = request.FILES.get("imgFile", None)
    if files:
        result = image_upload(files, dir_name)
    return HttpResponse(json.dumps(result), content_type="application/json")


# 目录创建
def upload_generation_dir(dir_name):
    today = dt.datetime.today()
    url_part = dir_name + '/%d/%d/' % (today.year, today.month)
    dir_name = os.path.join(dir_name, str(today.year), str(today.month))
    print("*********", os.path.join(settings.MEDIA_ROOT, dir_name))
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, dir_name)):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, dir_name))
    return dir_name,url_part


# 图片上传
def image_upload(files, dir_name):
    # 允许上传文件类型
    allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
    file_suffix = files.name.split(".")[-1]
    if file_suffix not in allow_suffix:
        return {"error": 1, "message": "图片格式不正确"}
    relative_path_file, url_part = upload_generation_dir(dir_name)
    path = os.path.join(settings.MEDIA_ROOT, relative_path_file)
    print("&&&&path", path)
    if not os.path.exists(path): # 如果目录不存在创建目录
        os.makedirs(path)
    file_name = str(uuid.uuid1()) + "." + file_suffix
    path_file = os.path.join(path, file_name)
    file_url =settings.MEDIA_URL + url_part +file_name
    open(path_file, 'wb').write(files.file.read())
    return {"error": 0, "url": file_url}



