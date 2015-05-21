from rest_framework import serializers
from api.generics import utils
from rest_framework.pagination import PaginationSerializer

# class DynamicFieldsModelSerializer(serializers.ModelSerializer):
#     """
#     ModelSerializer taking an extra `fields` paramater, to indicate which fields to show
#     """

#     def __init__(self, *args, **kwargs):
#         # Don't pass the 'fields' arg up to the superclass
#         fields = kwargs.pop('fields', None)

#         # Instantiate the superclass normally
#         super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

#         if fields is not None:
#             # Drop any fields that are not specified in the `fields` argument.
#             allowed = set(fields)
#             existing = set(self.fields.keys())
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)

class DynamicFields(object):

    @property
    def is_root_dynamic_fields(self):
        """
        Returns true if the current DynamicFields serializer is the root
        DynamicFields serializer.
        """
        parent = self.parent
        root = self.root
        result = None

        if parent is None:
            return True

        while result is None:
            if root == parent or not hasattr(parent, 'parent'):
                result = True
            if isinstance(parent, DynamicFields):
                result = False
            else:
                parent = parent.parent
        return result

    def __init__(self, *args, **kwargs):
        self.query_field = kwargs.pop('query_field', 'fields')
        self._selected_fields = kwargs.pop('fields', None)
        self.fields_selected = False

        super(DynamicFields, self).__init__(*args, **kwargs)

    def _selected_fields_from_query_params(self, query_params):
        selected_fields = []

        if self.query_field in query_params:
            selected_fields = query_params[self.query_field].split(',')

        fields_dict = utils.get_type_parameters(self.query_field, query_params)
        for k, v in fields_dict.items():
            if k in self.fields.keys():
                selected_fields.append(k)
                self.fields[k].selected_fields = v.split(',')

        return selected_fields

    @property
    def selected_fields(self):
        """
        Returns the selected fields in the DynamicFieldsSerializer.
        """
        query_params = utils.query_params_from_context(self.context)
        view = self.context.get('view')

        if self.is_root_dynamic_fields:
            # if view and self._selected_fields is None:
            #     fields = getattr(view, 'fields', None)
            #     if fields:
            #         self._selected_fields = fields

            if query_params:
                fields = self._selected_fields_from_query_params(query_params)
                if fields:
                    self._selected_fields = fields

        if self._selected_fields and not isinstance(
                self._selected_fields, (list, tuple)):
            raise TypeError(
                'The `fields` option must be a list or tuple. Got %s.' %
                type(self._selected_fields).__name__
            )

        return self._selected_fields

    @selected_fields.setter
    def selected_fields(self, fields):
        self._selected_fields = fields

    def select_fields(self):
        if self.selected_fields is not None:
            keep_fields = set(self.selected_fields)
            all_fields = set(self.fields.keys())
            for field_name in all_fields - keep_fields:
                del self.fields[field_name]

    def to_representation(self, instance):
        if not self.fields_selected:
            self.select_fields()
            self.fields_selected = True
        return super(DynamicFields, self).to_representation(instance)


class DynamicFieldsSerializer(DynamicFields, serializers.Serializer):
    def __init__(self, *args, **kwargs):
        # Instantiate mixin, superclass
        super(DynamicFieldsSerializer, self).__init__(*args, **kwargs)


class DynamicFieldsModelSerializer(DynamicFields, serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Instantiate mixin, superclass
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)


class NoCountPaginationSerializer(PaginationSerializer):
    """
    PaginationSerializer that removes the count field when specified in the
    query_params.
    """
    def __init__(self, *args, **kwargs):
        super(NoCountPaginationSerializer, self).__init__(*args, **kwargs)
        query_params = utils.query_params_from_context(self.context)
        if 'nocount' in query_params:
            del self.fields['count']
