from django.contrib import admin
from .models import *
class PostAdmin(admin.ModelAdmin):
    class Media:
        js=(
            'js/editor/kindeditor-all.js',
            'js/editor/config.js',
        )

admin.site.register(Banner)
admin.site.register(BlogCategory)
admin.site.register(Tags)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
admin.site.register(FriendlyLink)
# Register your models here.
