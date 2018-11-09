from django.shortcuts import render
from .models import AreaInfo
from django.http import JsonResponse
from django.conf import settings
from django.http    import HttpResponse
from django.core.paginator import Paginator
def area(resquest):
    area=AreaInfo.objects.get(pk=440100)
    ctx={
        'area': area
    }
    return render(resquest,'booktest/area.html',ctx)


def area1(request):
    return render(request,'booktest/area1.html')

def area2(request):
    list = AreaInfo.objects.filter(aParent__isnull=True)
    list2 = []
    for item in list:
        list2.append([item.id, item.atitle])
    return JsonResponse({'data': list2})

#获取省信息
def area3(request, pid):
    list = AreaInfo.objects.filter(aParent_id=pid)
    list2 = []
    for item in list:
        list2.append([item.id, item.atitle])
    return JsonResponse({'data': list2})
# Create your views here.
#分页
def page_text(request,p):
    list=AreaInfo.objects.all()
    paginator=Paginator(list,100)
    if p == '':
        p=1
    list1=paginator.page(int(p))
    ctx={
        'list1':list1,
        'paginator':paginator,
    }
    return render(request,'booktest/index1.html',ctx)

