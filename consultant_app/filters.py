import django_filters

from .models import *
from django_filters.filters import Filter, CharFilter, BooleanFilter, \
    ChoiceFilter, DateFilter, DateTimeFilter, TimeFilter, ModelChoiceFilter, \
    ModelMultipleChoiceFilter, NumberFilter


class TechnologyFilter(django_filters.rest_framework.FilterSet):
    technology = django_filters.CharFilter(name="technology",lookup_expr='icontains')

    class Meta:
        model = Technology
        fields = ['technology',]





    # class TechnologyFilter(django_filters.FilterSet):
#     # default for CharFilter is to have exact lookup_type
#     technology = django_filters.CharFilter(lookup_type='icontains')
#     print("llllllllllllllllll",technology.filter(technology='java'))

# class TechnologyFilter(django_filters.FilterSet):
    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # class Meta:
    #     model = Technology
        # fields = {"technology": ['exact', 'contains', 'in', 'startswith']}
        # fields =['technology',]
        # fields = {
        #     'technology': ['icontains'],
        # }
        # filter_overrides = {
        #     models.CharField: {
        #         'filter_class': django_filters.CharFilter,
        #         'extra': lambda f: {
        #             'lookup_expr': 'icontains',
        #         },
        #     },}
    # technology = django_filters.rest_framework.CharFilter(lookup_expr='icontains')


    # print("llllllllllllllllll",technology)



    # class Meta:
    #     model = Technology
        # fields = {"technology": ['exact', 'contains', 'in', 'startswith']}
        # fields =['technology',]
        # fields = {
        #     'technology': ['icontains'],
        # }


        # first_name=User.objects.filter(role='supporter')
    # print("first_name  first_name",first_name)

    # tricky part - how to filter by related field?
    # but not by its foreign key (default)
    # `to_field_name` is crucial here
    # `conjoined=True` makes that, the more tags, the more narrow the search
    # tags = django_filters.CharFilter(
    #     queryset=User.objects.all(),
        # to_field_name='text',
        # conjoined=True,
    # )

    # class Meta:
    #     model = Technology
    #     fields =['technology',]


#
# class AllDjangoFilterBackend(DjangoFilterBackend):
#     """
#     A filter backend that uses django-filter.
#     """
#
#     def get_filter_class(self, view, queryset=User.objects.filter(role='supporter')):
#         """
#         Return the django-filters `FilterSet` used to filter the queryset.
#         """
#         filter_class = getattr(view, 'AllDjangoFilterBackend', None)
#         filter_fields = getattr(view, 'first_name', None)
#
#         if filter_class or filter_fields:
#             return super(AllDjangoFilterBackend, self).get_filter_class(self, view, queryset=queryset)
#
#         class AutoFilterSet(self.default_filter_set):
#             class Meta:
#                 model = User
#                 fields = ('first_name',)
#
#         return AutoFilterSet