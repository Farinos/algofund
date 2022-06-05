from attr import fields
from .models import Pool
from rest_framework import serializers

class PoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pool
        fields = ('id', 'name', 'description', 'applicationIndex', 'image')