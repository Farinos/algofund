from account import Account
from .models import Fund, FundWithdraw, Pool
from rest_framework import serializers

class PoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pool
        fields = ('id', 'name', 'description', 'applicationIndex', 'minAmount', 'expiryTime', 'image')

class FundSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Fund
        fields = ('senderMnemonic', 'amount')

class FundWithdrawSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FundWithdraw
        fields = ('requesterMnemonic',)