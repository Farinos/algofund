from account import Account
from util import ContractUtils
from operations import createDonationPool, fundPool, withdrawFunds
from .apps import ApiConfig

from .serializers import FundSerializer, FundWithdrawSerializer, PoolSerializer
from .models import Pool
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import Http404, QueryDict
from django.shortcuts import render

from datetime import datetime

# Create api view with customizable json
@api_view(['GET','POST'])
def list_pool(request):
    if request.method == 'GET':
        pools = Pool.objects.all().order_by('name')
        serializer = PoolSerializer(pools, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = PoolSerializer(data=request.data)
        mnemonic = request.data['creatorMnemonic']
        print(request.data)
        if serializer.is_valid():
            poolData = request.data
            if isinstance(poolData, QueryDict) and not poolData._mutable: poolData._mutable = True
            expiryTimestamp = int(datetime.strptime(poolData['expiryTime'], '%Y-%m-%d').timestamp())
            smartContractAddr = createDonationPool(ApiConfig.client, Account.FromMnemonic(mnemonic), poolData['minAmount'], expiryTimestamp)
            poolData['applicationIndex'] = smartContractAddr
            serializer = PoolSerializer(data=poolData)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET',])
def pool_details(request, pk):
    try:
        pool = Pool.objects.get(pk=pk)
    except Pool.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PoolSerializer(pool)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def pool_funds(request, pk):
    pool: Pool
    try:
        pool = Pool.objects.get(pk=pk)
    except Pool.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        serializer = FundSerializer(data=request.data)
        if serializer.is_valid():
            senderMnemonic = request.data['senderMnemonic']
            try:    
                amount = int(request.data['amount'])
            except:
                amount = request.data['amount']
            if fundPool(ApiConfig.client, Account.FromMnemonic(senderMnemonic), ContractUtils.get_application_address(int(pool.applicationIndex)), amount) == None: return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def pool_withdraw(request, pk):
    pool: Pool
    try:
        pool = Pool.objects.get(pk=pk)
    except Pool.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'POST':
        serializer = FundWithdrawSerializer(data=request.data)
        if serializer.is_valid():
            if withdrawFunds(ApiConfig.client, pool.applicationIndex, Account.FromMnemonic(request.data['requesterMnemonic'])):
                return Response(data={'message': 'Withdraw completed'}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def pools(request):
    return render(request, "pools/pools.html", {
        "pools": Pool.objects.all(),
        "accounts": ContractUtils.getAddresses()
    })

def pool(request, pool_id):
    try:
        pool = Pool.objects.get(id=pool_id)
    except Pool.DoesNotExist:
        raise Http404("Pool not found.")
    return render(request, "pools/pool.html", {
        "pool": pool,
        "accounts": ContractUtils.getAddresses()
    })

@api_view(['GET'])
def addresses(request):
    if request.method == 'GET':
        addresses = [a.__dict__ for a in ContractUtils.getAddresses()]
        return Response(data=addresses, status=status.HTTP_200_OK)

# ONLY FOR TEST purposes
# ModelViewSet is a special view provided by Django Rest Framework that handles GET and POST for Pools
class PoolViewSet(viewsets.ModelViewSet):
    queryset = Pool.objects.all().order_by('name')
    serializer_class = PoolSerializer

    def create(self, request, *args, **kwargs):
        #print(request.data)
        #createDonationPool()
        #print(ApiConfig.client.account_application_info)
        return super().create(request, *args, **kwargs)