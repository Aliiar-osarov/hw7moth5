from decimal import Decimal

from rest_framework import serializers

from .models import Service, Order


class ServiceSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    orders_count = serializers.IntegerField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Service
        fields = [
            'id',
            'title',
            'description',
            'category',
            'price',
            'discount',
            'final_price',
            'is_available',
            'author',
            'created_at',
            'orders_count',
        ]
        read_only_fields = [
            'id',
            'author',
            'final_price',
            'created_at',
            'orders_count',
        ]

    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                'Название должно содержать минимум 5 символов.'
            )
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Цена должна быть больше 0.'
            )
        return value

    def validate_discount(self, value):
        if value < 0 or value > 90:
            raise serializers.ValidationError(
                'Скидка должна быть от 0 до 90%.'
            )
        return value

    def get_final_price(self, obj):
        return obj.price * Decimal(100 - obj.discount) / Decimal(100)


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'id',
            'service',
            'client_name',
            'phone',
            'comment',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
        ]