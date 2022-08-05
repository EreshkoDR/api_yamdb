from rest_framework import mixins, filters, viewsets

from .permissions import ReadOrAdminPermission


class ListCreateDestroyMixins(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (ReadOrAdminPermission,)
