from django_filters import rest_framework as filters

from ..models import Post


class PostFilter(filters.FilterSet):
    date__gte = filters.NumericRangeFilter(field_name="pub_date",
                                           lookup_expr='gte')
    date__lte = filters.NumericRangeFilter(field_name="pub_date",
                                           lookup_expr='lte')

    class Meta:
        model = Post
