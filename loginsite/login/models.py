from django.db import models
class User(models.Model):
    # 性别
    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True)
    # 密码我们建议最少128位
    password = models.CharField(max_length=256)
    # 内置邮箱字段,并且唯一
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # 使用str帮助人性化显示对象信息
        return self.name

    class Meta:
        # (元选项/元信息/元数据)里面定义用户按照时间的反序排列
        ordering = ['-c_time']
        verbose_name = '用户'
        verbose_name_plural = verbose_name
# Create your models here.
