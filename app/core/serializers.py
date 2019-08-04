from django.contrib.gis.geos import Polygon
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from core.models import Provider, ServiceArea


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'


class ServiceAreaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ServiceArea
        geo_field = 'polygon'
        fields = ('provider', 'name', 'price', 'polygon')

    def create(self, validated_data, instance=None):
        service_area = ServiceArea()
        service_area.name = validated_data.pop('name')
        service_area.price = validated_data.pop('price')
        service_area.provider = validated_data.pop('provider')
        geo_json = validated_data.pop('polygon')

        coords_ext = ()
        coords_int = []
        polygon_count = 0

        for feature in geo_json['features']:
            if feature['geometry']['type'] == "Polygon":
                for coordinate in feature['geometry']['coordinates']:
                    polygon_count += 1
                    if polygon_count == 1:
                        coords_ext += tuple(coordinate)
                    else:
                        coords_int.append(tuple(coordinate))

        service_area.polygon = Polygon(coords_ext, *coords_int)
        service_area.save()
        return service_area
