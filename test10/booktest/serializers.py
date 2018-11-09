from rest_framework import serializers
from . import models

class PublisherSerializer(serializers.ModelSerializer):
    #读取用户
    operator = serializers.ReadOnlyField(source='operator.username')
    class Meta:
        model = models.Publisher
        fields = (
            'id',
            'name',
            'address',
            'operator',
        )
class BookSerializer(serializers.HyperlinkedModelSerializer):
    publisher_name = serializers.StringRelatedField(source='publisher.name')

    class Meta:
        model = models.Book
        fields = (
            'id',
            'title',
            'publisher',
            'publisher_name',
        )






















