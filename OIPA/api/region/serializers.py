from rest_framework import serializers
import geodata
import iati.models
from api.generics.serializers import DynamicFieldsModelSerializer
from api.fields import GeometryField
from api.activity.aggregation import AggregationsSerializer

from api.generics import utils

class RegionVocabularySerializer(serializers.ModelSerializer):
    code = serializers.CharField()

    class Meta:
        model = iati.models.RegionVocabulary
        fields = ('code',)


class BasicRegionSerializer(DynamicFieldsModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='region-detail')
    code = serializers.CharField()
    region_vocabulary = RegionVocabularySerializer()

    class Meta:
        model = geodata.models.Region
        fields = (
            'url',
            'code',
            'name',
            'region_vocabulary'
        )


class RegionSerializer(DynamicFieldsModelSerializer):
    child_regions = BasicRegionSerializer(
        many=True, source='region_set', fields=('url', 'code', 'name'))
    parental_region = BasicRegionSerializer(fields=('url', 'code', 'name'))
    countries = serializers.HyperlinkedIdentityField(
        view_name='region-countries')
    location = GeometryField(source='center_longlat')

    activities = serializers.SerializerMethodField()
    aggregations = serializers.SerializerMethodField()

    def get_activities(self, obj):
        from api.activity.serializers import ActivitySerializer
        serializer = ActivitySerializer(utils.filter_activities_by_context(self, 'recipient_region', obj),
                                        # context={'request': self.context['request']},
                                        fields=(()),
                                        many=True)

        return serializer.data

    def get_aggregations(self, obj):
        from api.activity.serializers import ActivitySerializer
        fields = tuple(utils.query_params_from_context(self.context).get('aggregations', str()).split(','))

        serializer = AggregationsSerializer(
            utils.filter_activities_by_context(self, 'recipient_region', obj),
            fields=fields
        )

        return serializer.data


    class Meta:
        model = geodata.models.Region
        fields = (
            'url',
            'code',
            'name',
            'region_vocabulary',
            'parental_region',
            'countries',
            'activities',
            'location',
            'child_regions',
            'aggregations'
        )
