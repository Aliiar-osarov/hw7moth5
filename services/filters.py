import django_filters

from .models import Service


class ServiceFilter(django_filters.FilterSet):

    category = django_filters.CharFilter(
        field_name='category'
    )

    is_available = django_filters.BooleanFilter(
        field_name='is_available'
    )

    class Meta:
        model = Service
        fields = [
            'category',
            'is_available',
        ]