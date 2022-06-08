from algofund.account import Account
from operations import createDonationPool
from .apps import ApiConfig

from .serializers import PoolSerializer
from .models import Pool
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['POST'])
def post_pool(request):
    if request.method == 'POST':
        serializer = PoolSerializer(data=request.data)
        mnemonic = request.data['creator_mnemonic']
        print(request.data['creator_mnemonic'])
        if serializer.is_valid():
            createDonationPool(ApiConfig.client, Account.FromMnemonic(mnemonic))
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ModelViewSet is a special view provided by Django Rest Framework that handles GET and POST for Pools
class PoolViewSet(viewsets.ModelViewSet):
    queryset = Pool.objects.all().order_by('name')
    serializer_class = PoolSerializer

    def create(self, request, *args, **kwargs):
        createDonationPool()
        print(ApiConfig.client.account_application_info)
        return super().create(request, *args, **kwargs)