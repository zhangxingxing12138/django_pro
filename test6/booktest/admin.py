from django.contrib import admin

from .models import *
class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['id','gcontent']
class TestModelAdmin(admin.ModelAdmin):
    list_display = ['id','title']

admin.site.register(GoodsInfo,GoodsInfoAdmin)
admin.site.register(TestModel,TestModelAdmin)

# Register your models here.
