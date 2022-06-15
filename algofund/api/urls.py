from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'pools-viewset', views.PoolViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('pools/', views.list_pool),
    path('pools/<int:pk>', views.pool_details),
    path('pools/<int:pk>/funds', views.pool_funds, name="funds"),
    path('addresses/', views.addresses),
    path('views/pools/', views.pools, name="pools"),
    path('views/pools/<int:pool_id>', views.pool, name="pool"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]