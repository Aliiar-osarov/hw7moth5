from django.urls import path

from .views import (
    ServiceListCreateView,
    ServiceDetailView,
    TopServicesView,
    OrderListCreateView,
    OrderDetailView,
)


urlpatterns = [
    path(
        'services/',
        ServiceListCreateView.as_view(),
        name='service-list'
    ),

    path(
        'services/top/',
        TopServicesView.as_view(),
        name='service-top'
    ),

    path(
        'services/<int:pk>/',
        ServiceDetailView.as_view(),
        name='service-detail'
    ),

    path(
        'orders/',
        OrderListCreateView.as_view(),
        name='order-list'
    ),

    path(
        'orders/<int:pk>/',
        OrderDetailView.as_view(),
        name='order-detail'
    ),
]