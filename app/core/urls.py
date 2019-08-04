from django.conf.urls import url
from django.urls import path
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from core.views import ProviderViewSet, ServiceAreaViewSet, QueryServiceAreas

router = routers.DefaultRouter()
router.register(r'providers', ProviderViewSet)
router.register(r'serviceareas', ServiceAreaViewSet)

schema_view = get_swagger_view(title='API Docs')

urlpatterns = [
    path('serviceareas/by-lat-lon/<lat>/<lon>/', QueryServiceAreas.as_view(), name="query-service-area"),
    url(r'^docs/', schema_view),
]

urlpatterns += router.urls
