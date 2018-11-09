from django.contrib import admin

from .models import User
import hashlib
def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()
class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.password=hash_code(request.POST['password'])
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(User,UserAdmin)

# Register your models here.
