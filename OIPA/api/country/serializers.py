from rest_framework import serializers
import geodata
from api.generics.serializers import DynamicFieldsModelSerializer
from api.region.serializers import RegionSerializer
from api.fields import JSONField
from api.activity.aggregation import AggregationsSerializer

from api.generics import utils

class CountrySerializer(DynamicFieldsModelSerializer):
    class BasicCitySerializer(serializers.ModelSerializer):
        url = serializers.HyperlinkedIdentityField(view_name='city-detail')

        class Meta:
            model = geodata.models.City
            fields = (
                'url',
                'id',
                'name'
            )

    url = serializers.HyperlinkedIdentityField(view_name='country-detail')
    region = RegionSerializer(fields=('url', 'code', 'name'))
    un_region = RegionSerializer(fields=('url', 'code', 'name'))
    unesco_region = RegionSerializer(fields=('url', 'code', 'name'))
    capital_city = BasicCitySerializer()
    location = JSONField(source='center_longlat.json')
    polygon = JSONField()
    indicators = serializers.HyperlinkedIdentityField(
        view_name='country-indicators')
    cities = serializers.HyperlinkedIdentityField(view_name='country-cities')

    activities = serializers.SerializerMethodField()
    aggregations = serializers.SerializerMethodField()

    def get_activities(self, obj):
        from api.activity.serializers import ActivitySerializer
        serializer = ActivitySerializer(utils.filter_activities_by_context(self, 'recipient_country', obj),
                                        # context={'request': self.context['request']},
                                        fields=(()),
                                        many=True)

        print(serializer.data)
        return serializer.data 

    def get_aggregations(self, obj):
        from api.activity.serializers import ActivitySerializer
        fields = tuple(utils.query_params_from_context(self.context).get('aggregations', str()).split(','))

        serializer = AggregationsSerializer(
            utils.filter_activities_by_context(self, 'recipient_country', obj),
            fields=fields
        )

        return serializer.data

    class Meta:
        model = geodata.models.Country
        fields = (
            'url',
            'code',
            'numerical_code_un',
            'name',
            'alt_name',
            'language',
            'capital_city',
            'region',
            'un_region',
            'unesco_region',
            'dac_country_code',
            'iso3',
            'alpha3',
            'fips10',
            'data_source',
            'activities',
            'indicators',
            # 'adm1region_set',
            'cities',
            'aggregations',
            'location',
            'polygon',
        )
