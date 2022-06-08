from .apps import ApiConfig

from .serializers import PoolSerializer
from .models import Pool
from rest_framework import viewsets

# Create your views here.
# ModelViewSet is a special view provided by Django Rest Framework that handles GET and POST for Pools
class PoolViewSet(viewsets.ModelViewSet):
    queryset = Pool.objects.all().order_by('name')
    serializer_class = PoolSerializer

    def create(self, request, *args, **kwargs):
        #createDonationPool()
        print(ApiConfig.client.account_application_info)
        return super().create(request, *args, **kwargs)