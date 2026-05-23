from django.conf import settings
from django.db import models


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('starter', 'Закуски'),
        ('main', 'Основні страви'),
        ('dessert', 'Десерти'),
        ('drink', 'Напої'),
    ]

    name = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    image_url = models.URLField(blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class WorkingHours(models.Model):
    day = models.CharField(max_length=20)
    open_time = models.TimeField()
    close_time = models.TimeField()
    is_closed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Working hours'
        ordering = ['id']

    def __str__(self):
        if self.is_closed:
            return f'{self.day}: closed'
        return f'{self.day}: {self.open_time:%H:%M}-{self.close_time:%H:%M}'


class Hall(models.Model):
    name = models.CharField(max_length=100)
    zone = models.CharField(max_length=80)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.zone})'


class RestaurantTable(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='tables')
    number = models.PositiveIntegerField()
    seats = models.PositiveIntegerField()
    x = models.PositiveIntegerField(default=1)
    y = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['hall__name', 'number']
        unique_together = ['hall', 'number']

    def __str__(self):
        return f'Table {self.number} - {self.hall.name}'


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(RestaurantTable, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']
        unique_together = ['table', 'date', 'time']

    def __str__(self):
        return f'{self.customer_name}: table {self.table.number} on {self.date} {self.time:%H:%M}'

# Create your models here.
