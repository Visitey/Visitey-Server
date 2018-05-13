# from django_filters import rest_framework as filters
#
# class IsOwnerFilterBackend(filters.BaseFilterBackend):
#     """
#     Filter that only allows users to see their own objects.
#     """
#
#     def filter_queryset(self, request, queryset, view):
#         return queryset.filter(owner=request.user)
#
#
# class IsInRangeFilterBackend(filters.FilterSet):
#     """
#     Filter that return all events in range
#     """
#
#     def filter_queryset(self, request, queryset, view):
#         return queryset.filter(owner=request.user)
