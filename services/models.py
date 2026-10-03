from django.conf import settings
from django.db import models


class Service(models.Model):

    class Category(models.TextChoices):
        REPAIR = 'Ремонт', 'Ремонт'
        CLEANING = 'Уборка', 'Уборка'
        EDUCATION = 'Обучение', 'Обучение'
        BEAUTY = 'Красота', 'Красота'
        IT = 'IT', 'IT'
        OTHER = 'Другое', 'Другое'

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=Category.choices
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    discount = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Order(models.Model):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    client_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client_name} — {self.service.title}'