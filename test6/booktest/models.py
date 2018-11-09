from django.db import models
from tinymce.models import HTMLField
from ckeditor_uploader.fields import RichTextUploadingField
class GoodsInfo(models.Model):
    gcontent=HTMLField()


class TestModel(models.Model):
    title=models.CharField(max_length=50)
    content=RichTextUploadingField()
# Create your models here.
