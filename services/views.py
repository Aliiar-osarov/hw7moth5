from django.core.cache import cache
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Service, Order
from .serializers import ServiceSerializer, OrderSerializer
from .permissions import IsOwnerOrAdmin, OrderPermission
from .filters import ServiceFilter


class ServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsOwnerOrAdmin]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = ServiceFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return (
            Service.objects
            .annotate(orders_count=Count('orders'))
            .select_related('author')
            .all()
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        cache.delete('top_services')


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        return (
            Service.objects
            .annotate(orders_count=Count('orders'))
            .select_related('author')
            .all()
        )

    def perform_update(self, serializer):
        serializer.save()
        cache.delete('top_services')

    def perform_destroy(self, instance):
        cache.delete('top_services')
        instance.delete()


class TopServicesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cache_key = 'top_services'

        data = cache.get(cache_key)

        if data is None:
            services = (
                Service.objects
                .filter(is_available=True)
                .annotate(orders_count=Count('orders'))
                .order_by(
                    '-orders_count',
                    '-created_at'
                )[:5]
            )

            data = ServiceSerializer(
                services,
                many=True
            ).data

            cache.set(
                cache_key,
                data,
                300
            )

        return Response(data)


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [OrderPermission]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.select_related(
                'service',
                'service__author'
            ).all()

        return Order.objects.filter(
            service__author=self.request.user
        ).select_related('service')

    def perform_create(self, serializer):
        serializer.save()
        cache.delete('top_services')


class OrderDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [OrderPermission]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.select_related(
                'service',
                'service__author'
            ).all()

        return Order.objects.filter(
            service__author=self.request.user
        ).select_related('service')

    def perform_destroy(self, instance):
        cache.delete('top_services')
        instance.delete()