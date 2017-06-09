from rest_framework import filters, viewsets

from pretix.api.filters.ordering import ExplicitOrderingFilter
from pretix.api.serializers.item import (
    ItemCategorySerializer, ItemSerializer, QuestionSerializer,
    QuotaSerializer,
)
from pretix.base.models import Item, ItemCategory, Question, Quota


class ItemFilter(filters.FilterSet):
    class Meta:
        model = Item
        fields = ['active', 'category', 'admission', 'tax_rate', 'free_price']


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.none()
    filter_backends = (filters.DjangoFilterBackend, ExplicitOrderingFilter)
    ordering_fields = ('id', 'position')
    ordering = ('position', 'id')
    filter_class = ItemFilter

    def get_queryset(self):
        return self.request.event.items.prefetch_related('variations', 'addons').all()


class ItemCategoryFilter(filters.FilterSet):
    class Meta:
        model = ItemCategory
        fields = ['is_addon']


class ItemCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ItemCategorySerializer
    queryset = ItemCategory.objects.none()
    filter_backends = (filters.DjangoFilterBackend, ExplicitOrderingFilter)
    filter_class = ItemCategoryFilter
    ordering_fields = ('id', 'position')
    ordering = ('position', 'id')

    def get_queryset(self):
        return self.request.event.categories.all()


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.none()
    filter_backends = (ExplicitOrderingFilter,)
    ordering_fields = ('id', 'position')
    ordering = ('position', 'id')

    def get_queryset(self):
        return self.request.event.questions.prefetch_related('options').all()


class QuotaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuotaSerializer
    queryset = Quota.objects.none()
    filter_backends = (ExplicitOrderingFilter,)
    ordering_fields = ('id', 'size')
    ordering = ('id',)

    def get_queryset(self):
        return self.request.event.quotas.all()