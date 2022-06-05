from django.shortcuts import render
from .serializers import PoolSerializer
from .models import Pool
from rest_framework import viewsets

# Create your views here.
# ModelViewSet is a special view provided by Django Rest Framework that handles GET and POST for Pools
class PoolViewSet(viewsets.ModelViewSet):
    queryset = Pool.objects.all().order_by('name')
    serializer_class = PoolSerializer