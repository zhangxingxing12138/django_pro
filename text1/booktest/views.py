from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *


# Create your views here.
def index(request):

    list=BookInfo.objects.all()

    template=loader.get_template('booktest/index.html')


    #model


    #template
    ctx = {'list': list}
    return HttpResponse(template.render(ctx))
def show(request, bid):
    book=BookInfo.objects.get(id=bid)
    list=book.heroinfo_set.all()
    ctx={
        'list':list
    }
    return render(request,'booktest/hname.html',ctx)
