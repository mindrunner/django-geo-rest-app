from django.contrib.gis.geos import Point
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Provider, ServiceArea
from core.serializers import ProviderSerializer, ServiceAreaSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ServiceAreaViewSet(viewsets.ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer


class QueryServiceAreas(APIView):
    def get(self, request, format=None, lat=None, lon=None):
        try:
            p = Point(x=float(lat), y=float(lon))
            service_areas = ServiceArea.objects.filter(polygon__contains=p)
            serializer = ServiceAreaSerializer(service_areas, many=True)
            return Response(serializer.data)
        except Exception as e:
            data = {"message": e}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)