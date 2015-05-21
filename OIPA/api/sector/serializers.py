from rest_framework import serializers
import iati
from api.generics.serializers import DynamicFieldsModelSerializer
from api.activity.aggregation import AggregationsSerializer

from api.generics import utils

class SectorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = iati.models.SectorCategory
        fields = (
            'code',
        )


class SectorSerializer(DynamicFieldsModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='sector-detail')
    category = SectorCategorySerializer()

    activities = serializers.SerializerMethodField()
    aggregations = serializers.SerializerMethodField()

    def get_activities(self, obj):
        from api.activity.serializers import ActivitySerializer
        serializer = ActivitySerializer(utils.filter_activities_by_context(self, 'sector', obj),
                                        # context={'request': self.context['request']},
                                        fields=(()),
                                        many=True)

        return serializer.data

    def get_aggregations(self, obj):
        from api.activity.serializers import ActivitySerializer
        fields = tuple(utils.query_params_from_context(self.context).get('aggregations', str()).split(','))

        serializer = AggregationsSerializer(
            utils.filter_activities_by_context(self, 'sector', obj),
            fields=fields
        )

        return serializer.data


    class Meta:
        model = iati.models.Sector
        fields = (
            'url',
            'code',
            'name',
            'description',
            'category',
            'activities',
            'aggregations'
        )
