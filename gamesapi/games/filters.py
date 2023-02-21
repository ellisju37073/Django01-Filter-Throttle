from django_filters.rest_framework import DjangoFilterBackend


class AllDjangoFilterBackend(DjangoFilterBackend):
    """
    A filter backend that uses django-filter.
    """

    def get_filterset_class(self, view, queryset=None):
        '''
        Return the django-filters `FilterSet` used to filter the queryset.
        '''
        filter_class = getattr(view, 'filter_class', None)
        filter_fields = getattr(view, 'filter_fields', None)

        if filter_class or filter_fields:
            return super().get_filter_class(self, view, queryset)

        class AutoFilterSet(self.filterset_base):
            class Meta:
                fields = "__all__"
                model = queryset.model

        return AutoFilterSet