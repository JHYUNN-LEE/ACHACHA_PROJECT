import django_filters
from django_filters import DateFilter
from .models import LostItems

class Orderfilter(django_filters.FilterSet):
    class Meta:
        model = LostItems
        fields = {
            'get_at': ['icontains'],
            'name': ['icontains'],
        }

