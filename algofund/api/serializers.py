from attr import fields
from .models import Fund, Pool
from rest_framework import serializers

class PoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pool
        fields = ('id', 'name', 'description', 'applicationIndex', 'minAmount', 'expiryTime', 'image')

class FundSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Fund
        fields = ('senderMnemonic', 'amount')