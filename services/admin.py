from django.contrib import admin

from .models import Service, Order


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'category',
        'price',
        'discount',
        'is_available',
        'author',
        'created_at',
    )

    list_filter = (
        'category',
        'is_available',
    )

    search_fields = (
        'title',
        'description',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'service',
        'client_name',
        'phone',
        'created_at',
    )

    search_fields = (
        'client_name',
        'phone',
    )